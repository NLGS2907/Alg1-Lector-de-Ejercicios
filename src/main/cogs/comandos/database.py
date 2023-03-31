"""
Cog que agrupa comandos para interactuar con la DB.
"""

from io import BytesIO
from sqlite3 import OperationalError
from typing import TYPE_CHECKING, Any, Optional
from zipfile import ZIP_DEFLATED, ZipFile

from discord import File, Interaction
from discord.app_commands import Choice, autocomplete, choices
from discord.app_commands import command as appcommand
from discord.app_commands import describe
from discord.app_commands.errors import AppCommandError, CheckFailure

from ...auxiliar import autocompletado_nombres_tablas_db, verificar_rol
from ...db import (actualizar_dato_de_tabla, borrar_datos_de_tabla,
                   ejecutar_linea, insertar_datos_en_tabla,
                   sacar_datos_de_tabla)
from ...interfaces import LineaDB, ScriptDB
from ..general import CogGeneral, GroupsList, GrupoGeneral

if TYPE_CHECKING:
    from ...db import FetchResult
    from ...lector import Lector


class GrupoDB(GrupoGeneral):
    """
    Grupo para comandos que ejecutan comandos de SQLite3.
    """

    def __init__(self, bot: "Lector") -> None:
        """
        Inicializa una instancia de 'GrupoDB'.
        """

        super().__init__(bot,
                         name="db",
                         description="Comandos para ejecutar comandos a la DB.")


    async def interaction_check(self, interaccion: Interaction) -> bool:
        """
        Verifica si el usuario está autorizado.
        """

        return verificar_rol(interaccion)


    async def on_error(self, interaccion: Interaction, error: AppCommandError) -> None:
        """
        Avisa el usuario que un comando falló.
        """

        if isinstance(error, CheckFailure):
            mensaje = f"Nope, {interaccion.user.mention}, vos no podés tocar la base de datos "
            await interaccion.response.send_message(content=mensaje,
                                                    ephemeral=True)
            return

        raise error from error


    def _evaluar(self, dato: str) -> Any:
        """
        Lee un dato en string y lo convierte al tipo correspondiente.
        """

        def isfloat(d: str) -> bool:
            "Determina si un string es un decimal."

            try:
                float(d)
            except:
                return False
            else:
                return True

        cierra = lambda s, q : (s.startswith(q) and s.endswith(q))

        data = dato

        if data.isdigit():
            data = int(data)
        elif isfloat(data):
            data = float(data)
        elif cierra(data, "\"") or cierra(data, "\'"):
            data = data.strip("\"").strip("\'")

        return data


    def _procesar_conds(self, condiciones: str) -> dict:
        """
        Procesa un string en un diccionario apto para usar
        en comandos de la DB.
        """

        conds_strs = ''.join(condiciones.split()).split("--")
        conds = {}
        for cond in conds_strs:
            if not cond: # Un string vacío
                continue

            prop, val = cond.split("=")
            conds[self._evaluar(prop)] = self._evaluar(val)

        return conds


    def _procesar_res(self, res: "FetchResult") -> tuple[str, list[BytesIO]]:
        """
        Procesa resoluciones para poder mostrarse.
        """

        datos = []
        lista_archivos = []

        for dato in res:
            d = repr(dato)

            if isinstance(dato, bytes):
                b_len = len(dato)
                s = "" if b_len == 1 else "s"
                d = f"Blob de {len(dato)} byte{s}."

                arch = BytesIO(dato)
                arch.seek(0)
                lista_archivos.append(arch)

            datos.append(f"`{d}`")

        datos_str = ",\t".join(datos)
        return (f"({datos_str})", lista_archivos)


    def _procesar_arch(self, lista_arch: list[BytesIO], limite: int=10) -> list[BytesIO]:
        """
        Si la lista excede el límite de archivos, los comprime en un ZIP.
        """

        excede = len(lista_arch) > limite
        lista_final = []
        arch_zip = BytesIO()
        zf = ZipFile(arch_zip, mode="w", compression=ZIP_DEFLATED)

        for i, arch in enumerate(lista_arch):
            # No se puede adivinar la extensión
            nombre_dato = f"dato_{str(i).zfill(2)}"

            if excede:
                zf.writestr(nombre_dato, arch.read())
                arch.seek(0)
            else:
                lista_final.append(File(arch, filename=nombre_dato))
        
        zf.close()
        if excede:
            arch_zip.seek(0)
            lista_final = [File(arch_zip, filename="datos.zip")]

        return lista_final


    @appcommand(name="linea",
                description="Ejecuta una operación de una línea.")
    @describe(comando="El comando a ejecutar. Debe obedecer la sintaxis de SQLite3.")
    async def ejecutarlinea(self,
                            interaccion: Interaction,
                            comando: Optional[str]=None) -> None:
        """
        Ejecuta un comando de una línea.
        """

        if comando is None:
            await interaccion.response.send_modal(LineaDB())
            return

        msg = ""

        try:
            desc = ejecutar_linea(comando)
            filas = desc['rowcount']

            s = ('' if filas == 1 else 's')
            ron = ('' if filas == 1 else 'ron')
            msg_filas = f" `{filas}` *fila{s} fue{ron} afectada{s}.*"
            msg = f"*Operación exitosa.*{msg_filas if filas >= 0 else ''}"

        except SyntaxError:
            msg = "**[ERROR]:** *Sintaxis inválida.*"

        except OperationalError as e:
            msg = f"**[ERROR]:** {str(e)}"


        await interaccion.response.send_message(content=(msg
                                                         if msg.strip()
                                                         else "*Hmmm, parece que algo ocurrió.*"),
                                                ephemeral=True)


    @appcommand(name="script",
                description="Ejecuta un script de varias líneas.")
    async def ejecutarscript(self, interaccion: Interaction) -> None:
        """
        Ejecuta un comando de varias líneas.
        """

        await interaccion.response.send_modal(ScriptDB())


    @appcommand(name="fetch",
                description="Saca un dato de una tabla.")
    @describe(tabla="La tabla de donde sacar datos.",
              condiciones=("Las condiciones deben venir en el formato " +
                           "'prop1=val1 -- prop2=val2 -- ...'"),
              sacar_uno="Si sacar sólo un resultado o todos.")
    @choices(sacar_uno=[
        Choice(name="Uno solo", value=1),
        Choice(name="Todos", value=0)
    ])
    @autocomplete(tabla=autocompletado_nombres_tablas_db)
    async def dbfetch(self,
                      interaccion: Interaction,
                      tabla: str,
                      condiciones: str="",
                      sacar_uno: Choice[int]=0) -> None:
        """
        Saca datos de una tabla.
        """

        res_msg = ""
        cita = ">>> "

        try:
            conds = self._procesar_conds(condiciones)
            res = sacar_datos_de_tabla(tabla=tabla,
                                       sacar_uno=bool(sacar_uno.value
                                                      if isinstance(sacar_uno, Choice)
                                                      else sacar_uno),
                                       **conds)
            res = [res] if sacar_uno else res

            lista_datos = []
            lista_arch = []
            for r in res:
                datos, l_archs = self._procesar_res(r)
                lista_datos.append(f"- {datos}")
                lista_arch.extend(l_archs)


            res_msg = cita + "\n".join(lista_datos)

        except SyntaxError:
            res_msg = "**[ERROR]** `/db fetch`: *Sintaxis inválida.*"

        except OperationalError as e:
            res_msg = f"**[ERROR]** `/db fetch`: *{str(e)!r}*"

        res_msg_cap = res_msg if len(res_msg) < 2000 else f"{res_msg[:1995]}[...]"
        await interaccion.response.send_message(content=(res_msg_cap
                                                        if res_msg.lstrip(cita)
                                                        else "*No se encontró nada.*"),
                                                files=self._procesar_arch(lista_arch),
                                                ephemeral=True)


    @appcommand(name="delete",
                description="Borra un dato en una tabla.")
    @describe(tabla="La tabla de donde borrar datos.",
              condiciones=("Las condiciones deben venir en el formato " +
                           "'prop1=val1 -- prop2=val2 -- ...'"))
    @autocomplete(tabla=autocompletado_nombres_tablas_db)
    async def dbdelete(self,
                       interaccion: Interaction,
                       tabla: str,
                       condiciones: str) -> None:
        """
        Borra datos de una tabla.
        """

        res_msg = ""

        try:
            conds = self._procesar_conds(condiciones)
            filas = borrar_datos_de_tabla(tabla=tabla,
                                          **conds)
            s = ("" if filas == 1 else "s")
            ron = ("" if filas == 1 else "ron")
            res_msg = (f"*Operación realizada correctamente.*\n`{filas}` *fila{s} " +
                       f"fue{ron} afectada{s}.*")

        except SyntaxError:
            res_msg = "**[ERROR]** `/db delete`: *Sintaxis inválida.*"

        except OperationalError as e:
            res_msg = f"**[ERROR]** `/db delete`: *{str(e)!r}*"

        await interaccion.response.send_message(content=(res_msg
                                                        if res_msg.strip()
                                                        else "*Hmmm, parece que algo ocurrió.*"),
                                                ephemeral=True)


    @appcommand(name="insert",
                description="Inserta un dato en una tabla.")
    @describe(tabla="La tabla en donde sacar datos.",
              valores=("Los valores a insertar. Deben ser la misma cantidad que columnas " +
                       "tenga la tabla y obedecer el formato 'val1 -- val2 -- val3 -- ...'"),
              incluir_llave_primaria=("Si, al insertar datos, se cuenta el primer dato " +
                                      "como la llave primaria o si agregar uno por defecto."))
    @choices(incluir_llave_primaria=[
        Choice(name="No", value=0),
        Choice(name="Sí", value=1)
    ])
    @autocomplete(tabla=autocompletado_nombres_tablas_db)
    async def dbinsert(self,
                       interaccion: Interaction,
                       tabla: str,
                       valores: str,
                       incluir_llave_primaria: Choice[int]=1) -> None:
        """
        Inserta datos en una tabla.
        """

        res_msg = ""

        try:
            vals_strs = ''.join(valores.split()).split("--")
            vals = tuple(self._evaluar(val) for val in vals_strs if val)

            filas = insertar_datos_en_tabla(tabla=tabla,
                                            llave_primaria_por_defecto=bool(incluir_llave_primaria),
                                            valores=vals)
            s = ('' if filas == 1 else 's')
            ron = ("" if filas == 1 else "ron")
            res_msg = (f"*Valores* `{vals}` *insertados correctamente.*\n`{filas}` *fila{s} " +
                       f"fue{ron} afectada{s}.*")

        except SyntaxError:
            res_msg = "**[ERROR]** `/db insert`: *Sintaxis inválida.*"

        except OperationalError as e:
            res_msg = f"**[ERROR]** `/db insert`: *{str(e)!r}*"

        await interaccion.response.send_message(content=(res_msg
                                                        if res_msg.strip()
                                                        else "*Hmmm, parece que algo ocurrió...*"),
                                                ephemeral=True)


    @appcommand(name="update",
                description="Actualiza un dato en una tabla.")
    @describe(tabla="La tabla en la que actualizar el dato.",
              columna="El nombre de la columna de donde actualizar el dato.",
              valor="El valor actualizado.",
              condiciones=("Las condiciones deben venir en el formato " +
                           "'prop1=val1 -- prop2=val2 -- ...'"))
    @autocomplete(tabla=autocompletado_nombres_tablas_db)
    async def dbupdate(self,
                       interaccion: Interaction,
                       tabla: str,
                       columna: str,
                       valor: str,
                       condiciones: str) -> None:
        """
        Actualiza un dato en una tabla.
        """

        res_msg = ""

        try:
            conds = self._procesar_conds(condiciones)
            columna = self._evaluar(columna)
            valor = self._evaluar(valor)

            filas = actualizar_dato_de_tabla(tabla=tabla,
                                             nombre_col=columna,
                                             valor=valor,
                                             **conds)
            s = ('' if filas == 1 else 's')
            ron = ("" if filas == 1 else "ron")
            res_msg = (f"*Valor* `{valor}` *actualizado correctamente.*\n`{filas}` *fila{s} " +
                       f"fue{ron} afectada{s}.*")

        except SyntaxError:
            res_msg = "**[ERROR]** `/db update`: *Sintaxis inválida.*"

        except OperationalError as e:
            res_msg = f"**[ERROR]** `/db update`: *{str(e)!r}*"

        await interaccion.response.send_message(content=(res_msg
                                                        if res_msg.strip()
                                                        else "*Hmmm, parece que algo ocurrió...*"),
                                                ephemeral=True)


class CogDB(CogGeneral):
    """
    Cog para comandos de DB.
    """

    @classmethod
    def grupos(cls) -> GroupsList:
        """
        Devuelve la lista de grupos asociados a este Cog.
        """

        return [GrupoDB]


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogDB(bot))