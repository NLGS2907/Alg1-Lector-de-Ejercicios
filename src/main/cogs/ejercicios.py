"""
Cog para comandos de ejercicios.
"""

from random import choice
from typing import Optional

from discord.ext.commands import Context, check, command

from ..archivos.archivos import (DiccionarioGuia, actualizar_guia,
                                 lista_carpetas, lista_ejercicios,
                                 lista_unidades, version_es_valida)
from ..auxiliar.auxiliar import es_rol_valido
from ..constantes.constantes import MESSAGE_FORMAT
from ..interfaces.ui_ejercicios import NavegadorEjercicios, SelectorEjercicios
from ..interfaces.ui_unidades import SelectorGuia, SelectorUnidad
from ..logger.logger import log
from .general import CogGeneral


class CogEjercicios(CogGeneral):
    """
    Cog para comandos relacionados a los ejercicios y guías.
    """

    @staticmethod
    def existe_unidad(unidad: str, guia: DiccionarioGuia) -> bool:
        """
        Verifica si la unidad pasada existe dentro de la guía donde se guardan
        los ejercicios.

        Se sobreentiende que todas las claves de la guía son caracteres numéricos,
        y así debería mantenerse porque no se recomienda mutarlo.
        """

        return unidad and unidad in list(guia.keys())


    @staticmethod
    def existe_ejercicio(ejercicio: str, unidad: str, guia: DiccionarioGuia) -> tuple[bool, bool]:
        """
        Verifica si un determinado ejercicio existe en una determinada unidad.

        Devuelve uan tupla donde el primer elemento indica si existe la unidad
        especificada, mientras que el segundo especifica si existe el ejercicio
        especificado. Si no existe la unidad, tampoco el ejercicio.
        """

        if not CogEjercicios.existe_unidad(unidad, guia):

            return False, False

        return True, ejercicio and ejercicio in list(guia[unidad].keys())


    @staticmethod
    async def mostrar_unidad_y_ejercicio_validos(ctx: Context,
                                                 unidad: Optional[str],
                                                 ejercicio: Optional[str]) -> bool:
        """
        Muestra por pantalla errores que le indican al usuario si los valores
        ingresados para la unidad y el ejercicio son inválidos.
        """

        guia = ctx.bot.guias[str(ctx.guild.id)]

        unidad_existe, ej_existe = CogEjercicios.existe_ejercicio(ejercicio, unidad, guia)

        if not unidad_existe:

            if unidad is None:

                await ctx.channel.send(content="Por favor elija el número de unidad",
                                       view=SelectorUnidad(guia=guia))

            else:

                unidades = lista_unidades(guia)
                await ctx.channel.send(f"**[ERROR]** El número de unidad `{unidad}` no es válido."
                    + f"Los valores aceptados son:\n\n{' - '.join([f'`{u}`' for u in unidades])}")

            return False

        if not ej_existe:

            if ejercicio is None:

                await ctx.channel.send(content="Por favor elija un ejercicio",
                                       view=SelectorEjercicios(guia=guia, unidad=unidad))

            else:

                ejercicios = lista_ejercicios(guia, unidad)
                await ctx.channel.send(f"**[ERROR]** El número de ejercicio `{ejercicio}` no " +
                                       "es válido. Los valores aceptados son:\n\n" +
                                       f"{' - '.join([f'`{ej}`' for ej in ejercicios])}")

            return False

        return True


    @command(name="ej",
             aliases=["ejercicio", "enunciado"],
             usage="[unidad [ejercicio]]",
             help="Muestra ejercicios de la guía.")
    async def leer_ejercicio(self,
                             ctx: Context,
        	                 unidad: Optional[str]=None,
                             ejercicio: Optional[str]=None) -> None:
        """
        Lee un ejercicio y lo manda por el canal correspondiente.
        """

        guia = self.bot.guias[str(ctx.guild.id)]

        if not await CogEjercicios.mostrar_unidad_y_ejercicio_validos(ctx, unidad, ejercicio):

            return

        enunciado = guia[unidad][ejercicio]

        mensaje = MESSAGE_FORMAT.format(mention=ctx.author.mention,
                                        unidad=unidad,
                                        titulo=guia[unidad]["titulo"],
                                        ejercicio=ejercicio,
                                        enunciado=enunciado)

        vista = NavegadorEjercicios(guia=guia, unidad=unidad, ejercicio=ejercicio)

        await ctx.channel.send(mensaje, view=vista)


    @command(name="random",
             aliases=["aleatorio", 'r'],
             usage="[unidad posible [sentido]]",
             help="Muestra un ejercicio aleatorio de la guía.")
    async def ejercicio_al_azar(self,
                                ctx: Context,
                                unidad_posible: Optional[str]=None,
                                sentido: str='=') -> None:
        """
        Muestra un ejercicio al azar de la guía.

        Si 'unidad_posible' es pasada y es válida, busca con esa unidad como pivote,
        siguiendo las instrucciones de 'opcion':

        '=' busca ejercicios solamente dentro de 'unidad_posible'.

        '<' busca ejercicios en unidades anteriores a la especificada.

        '<=' busca ejercicios en unidades anteriores y también en la especificada.

        '>' busca ejercicios en unidades posteriores a la especificada.

        '>=' busca ejercicios en unidades posteriores y también en la especificada.

        Todo funciona siempre en cuando las claves de la guia sean caracteres numéricos.
        """

        guia = self.bot.guias[str(ctx.guild.id)]

        unidad_pivote = (unidad_posible
                         if CogEjercicios.existe_unidad(unidad_posible, guia)
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

            case _: return

        if expresion_busqueda:

            unidad_elegida = choice([unidad for unidad in list(guia.keys())[1:]
                                    if expresion_busqueda(int(unidad))])

        ejercicio_elegido = choice(list(guia[unidad_elegida].keys()))

        await self.leer_ejercicio(ctx,
                                  unidad=unidad_elegida,
                                  ejercicio=ejercicio_elegido)


    @command(name="guia",
             aliases=["guia_version", "gver"],
             usage="nueva_version",
             help="Cambia la versión de la guía.")
    @check(es_rol_valido)
    async def cambiar_version_guia(self, ctx: Context, nueva_version: Optional[str]=None) -> None:
        """
        Cambia la versión de la guía a utilizar, si dicha versión es válida.
        """

        versiones = " - ".join(f"`{version}`" for version in lista_carpetas())

        if nueva_version is not None and not version_es_valida(nueva_version):

            await ctx.channel.send(f"**[ERROR]** La versión especificada `{nueva_version}` " +
                                   f"no es válida.\nLas versiones válidas son:\n{versiones}",
                                   delete_after=10.0)
            return

        version_vieja = self.bot.guias[str(ctx.guild.id)]["version"]

        if not nueva_version:

            await ctx.channel.send(content="Por favor seleccione una versión de la guía",
                                   view=SelectorGuia(version_actual=version_vieja))

        else:

            actualizar_guia(nueva_version, str(ctx.guild.id))
            await ctx.channel.send("**[AVISO]** La versión de la guía fue cambiada de " +
                                   f"`{version_vieja}` a `{nueva_version}` exitosamente.",
                                   delete_after=30.0)

        self.bot.actualizar_guia()

        formato_log = {"guild": ctx.guild.name,
                       "old_ver": version_vieja,
                       "new_ver": nueva_version}

        log.info("La versión de guía en '%(guild)s' fue cambiada de '%(old_ver)s' a '%(new_ver)s'",
                 formato_log)
