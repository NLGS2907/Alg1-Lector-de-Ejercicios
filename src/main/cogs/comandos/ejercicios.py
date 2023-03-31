"""
Cog para comandos de ejercicios.
"""

from random import choice
from typing import TYPE_CHECKING, Optional

from discord import Interaction
from discord.app_commands import Choice, choices
from discord.app_commands import command as appcommand
from discord.app_commands import describe

from ...archivos import (DiccionarioGuia, cargar_guia, get_guia_por_sv,
                         lista_carpetas, lista_ejercicios, lista_unidades,
                         version_es_valida)
from ...auxiliar import es_rol_valido
from ...db.atajos import (actualizar_version_guia, get_guia_default,
                          get_ruta_guia)
from ...embebido import Embebido
from ...interfaces import (TITLE_FORMAT, USER_CONSULT, NavegadorEjercicios,
                           SelectorEjercicios, SelectorGuia, SelectorUnidad)
from ..general import CogGeneral

if TYPE_CHECKING:

    from ...lector import Lector


class CogEjercicios(CogGeneral):
    """
    Cog para comandos relacionados a los ejercicios y guías.
    """

    @staticmethod
    def existe_unidad(unidad: Optional[str], guia: DiccionarioGuia) -> bool:
        """
        Verifica si la unidad pasada existe dentro de la guía donde se guardan
        los ejercicios.

        Se sobreentiende que todas las claves de la guía son caracteres numéricos,
        y así debería mantenerse porque no se recomienda mutarlo.
        """

        return unidad and unidad in list(guia)


    @staticmethod
    def existe_ejercicio(ejercicio: Optional[str],
                         unidad: Optional[str],
                         guia: DiccionarioGuia) -> tuple[bool, bool]:
        """
        Verifica si un determinado ejercicio existe en una determinada unidad.

        Devuelve uan tupla donde el primer elemento indica si existe la unidad
        especificada, mientras que el segundo especifica si existe el ejercicio
        especificado. Si no existe la unidad, tampoco el ejercicio.
        """

        if not CogEjercicios.existe_unidad(unidad, guia):

            return False, False

        return True, ejercicio and ejercicio in list(guia[unidad])


    async def mostrar_unidad_y_ejercicio_validos(self,
                                                 interaccion: Interaction,
                                                 unidad: Optional[str],
                                                 ejercicio: Optional[str]) -> bool:
        """
        Muestra por pantalla errores que le indican al usuario si los valores
        ingresados para la unidad y el ejercicio son inválidos.
        """

        guia = get_guia_por_sv(interaccion.guild_id)
        unidad_existe, ej_existe = CogEjercicios.existe_ejercicio(ejercicio, unidad, guia)

        if not unidad_existe:
            if unidad is None:
                vista = SelectorUnidad(guia=guia)
                await interaccion.response.send_message(
                                       content="Por favor elija el número de unidad",
                                       view=vista)

            else:

                unidades = lista_unidades(guia)
                self.bot.log.error(f"El número de unidad especificado '{unidad}' es inválido")
                await interaccion.response.send_message("**[ERROR]** El número de unidad " +
                                                        f"`{unidad}` no es válido. " +
                                                        "Los valores aceptados son:\n\n" +
                                                    f"{' - '.join([f'`{u}`' for u in unidades])}",
                                                        ephemeral=True)

            return False

        if not ej_existe:

            if ejercicio is None:

                vista = SelectorEjercicios(guia=guia, unidad=unidad)
                await interaccion.response.send_message(content="Por favor elija un ejercicio",
                                                        view=vista)

            else:

                ejercicios = lista_ejercicios(guia, unidad)
                self.bot.log.error(f"El número de ejercicio especificado '{ejercicio}' es inválido")
                await interaccion.response.send_message("**[ERROR]** El número de ejercicio " +
                                                        f"`{ejercicio}` no es válido. Los " +
                                                        "valores aceptados son:\n\n" +
                                                f"{' - '.join([f'`{ej}`' for ej in ejercicios])}",
                                                        ephemeral=True)

            return False

        return True


    async def mandar_ejercicio(self,
                               interaccion: Interaction,
        	                   unidad: Optional[str]=None,
                               ejercicio: Optional[str]=None) -> None:
        """
        Manda efectivamente el mensaje con el ejercicio por el canal.
        """

        guia = get_guia_por_sv(interaccion.guild_id)
        unidad = unidad or None

        if not await self.mostrar_unidad_y_ejercicio_validos(interaccion,
                                                             unidad,
                                                             ejercicio):
            return

        enunciado = guia[unidad][ejercicio]

        if not enunciado["titulo"]:
            enunciado["titulo"] = [TITLE_FORMAT.format(unidad=unidad,
                                                      titulo=guia[unidad]["titulo"],
                                                      ejercicio=ejercicio)]

        mensaje = USER_CONSULT.format(mencion=interaccion.user.mention)
        embebido = Embebido(opciones=enunciado)
        vista = NavegadorEjercicios(guia=guia, unidad=unidad, ejercicio=ejercicio)

        await interaccion.response.send_message(content=mensaje,
                                                embed=embebido,
                                                view=vista)


    @appcommand(name="ej",
                description="Muestra ejercicios de la guía.")
    @describe(unidad="El número de unidad.",
              ejercicio="El número de ejercicio.")
    @choices(unidad=[Choice(name=str(numero), value=str(numero))
                     for numero in lista_unidades(cargar_guia(get_guia_default()))])
    async def leer_ejercicio(self,
                             interaccion: Interaction,
        	                 unidad: Optional[Choice[str]]=None,
                             ejercicio: Optional[str]=None) -> None:
        """
        Lee un ejercicio y lo manda por el canal correspondiente.
        """

        await self.mandar_ejercicio(interaccion=interaccion,
                                    unidad=(unidad.value if unidad else None),
                                    ejercicio=ejercicio)


    @appcommand(name="random",
                description="Muestra un ejercicio aleatorio de la guía.")
    @describe(unidad_posible="La unidad desde dónde buscar.",
              sentido="El parámetro de búsqueda.")
    @choices(unidad_posible=[Choice(name=str(numero), value=str(numero))
                             for numero in lista_unidades(cargar_guia(get_guia_default()))],
             sentido=[
                 Choice(name="Dentro de", value='='),
                 Choice(name="Antes que", value='<'),
                 Choice(name="Antes o adentro de", value='<='),
                 Choice(name="Después que", value='>'),
                 Choice(name="Después o adentro de", value='>=')
             ])
    async def ejercicio_al_azar(self,
                                interaccion: Interaction,
                                unidad_posible: Optional[Choice[str]]=None,
                                sentido: Choice[str]='=') -> None:
        """
        Muestra un ejercicio al azar de la guía.

        Si 'unidad_posible' es pasada y es válida, busca con esa unidad como pivote,
        siguiendo las instrucciones de 'opcion':

        'Dentro de' busca ejercicios solamente dentro de 'unidad_posible'.

        'Antes que' busca ejercicios en unidades anteriores a la especificada.

        'Antes o adentro de' busca ejercicios en unidades anteriores y también en la especificada.

        'Después que' busca ejercicios en unidades posteriores a la especificada.

        'Después o adentro de' busca ejercicios en unidades posteriores y también en la
        especificada.

        Todo funciona siempre en cuando las claves de la guia sean caracteres numéricos.
        """

        guia = get_guia_por_sv(interaccion.guild_id)

        unidad_posible_real = (unidad_posible if unidad_posible is None else unidad_posible.value)
        unidad_pivote = (unidad_posible_real
                         if CogEjercicios.existe_unidad(unidad_posible_real, guia)
                         else choice(list(guia.keys())))
        expresion_busqueda = None
        unidad_elegida = ''
        ejercicio_elegido = ''

        match sentido:

            case '=':
                unidad_elegida = unidad_pivote
                ejercicio_elegido = choice(list(guia[unidad_pivote].keys()))

            case '<':
                expresion_busqueda = (lambda u: u < int(unidad_pivote))

            case "<=":
                expresion_busqueda = (lambda u: u <= int(unidad_pivote))

            case '>':
                expresion_busqueda = (lambda u: u > int(unidad_pivote))

            case ">=":
                expresion_busqueda = (lambda u: u >= int(unidad_pivote))

            case _:
                await interaccion.response.send_message("[ERROR] Algo salió mal.",
                                                        ephemeral=True)

        if expresion_busqueda:
            unidad_elegida = choice([unidad for unidad in list(guia.keys())[1:]
                                    if expresion_busqueda(int(unidad))])
        ejercicio_elegido = choice(list(guia[unidad_elegida].keys()))

        await self.mandar_ejercicio(interaccion,
                                    unidad=unidad_elegida,
                                    ejercicio=ejercicio_elegido)


    @appcommand(name="guia",
                description="Cambia la versión de la guía.")
    @describe(nueva_version="La nueva versión de la guía a configurar.")
    @choices(nueva_version=[Choice(name=nombre_unidad, value=nombre_unidad)
                            for nombre_unidad in lista_carpetas(get_ruta_guia())])
    @es_rol_valido()
    async def cambiar_version_guia(self,
                                  interaccion: Interaction,
                                  nueva_version: Optional[str]=None) -> None:
        """
        Cambia la versión de la guía a utilizar, si dicha versión es válida.
        """

        versiones = " - ".join(f"`{version}`" for version in lista_carpetas(get_ruta_guia()))

        if nueva_version is not None and not version_es_valida(nueva_version):

            await interaccion.response.send_message("**[ERROR]** La versión especificada " +
                                                    f"`{nueva_version}` no es válida.\nLas " +
                                                    f"versiones válidas son:\n{versiones}",
                                                    ephemeral=True)
            self.bot.log.error(f"La versión de la guía especificada '{nueva_version}' es inválida")
            return

        version_vieja = get_guia_por_sv(interaccion.guild_id)["version"]

        if not nueva_version:

            vista = SelectorGuia(version_actual=version_vieja)
            await interaccion.response.send_message(
                                        content="Por favor seleccione una versión de la guía",
                                        view=vista)

        else:

            actualizar_version_guia(nueva_version, interaccion.guild_id)

            self.bot.log.info(f"En '{interaccion.guild.name}', la versión de la guía fue " +
                              f"cambiada de '{version_vieja}' a '{nueva_version}' exitosamente")
            await interaccion.response.send_message("**[AVISO]** La versión de la guía fue " +
                                f"cambiada de `{version_vieja}` a `{nueva_version}` exitosamente.",
                                                    ephemeral=True)



async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogEjercicios(bot))
