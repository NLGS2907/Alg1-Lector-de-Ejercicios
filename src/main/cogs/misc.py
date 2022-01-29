"""
Cog para comandos misceláneos o de consultas.
"""

from discord.ext.commands import Context, command

from ..archivos.archivos import cargar_json
from ..auxiliar.auxiliar import mandar_dm
from ..constantes.constantes import INFO_MESSAGE, USER_CONSULT, WHATSNEW
from ..embebido.embebido import Embebido
from ..interfaces.ui_info import InfoUI
from .general import CogGeneral


class CogMisc(CogGeneral):
    """
    Cog para comandos misceláneos.
    """

    @command(name="info",
             aliases=["i"],
             usage="[-dm]",
             help="Muestra una lista de todos los comandos.")
    async def mostrar_info(self, ctx: Context, *opciones):
        """
        Muestra una lista con los comandos y lo que hace cada uno.
        """

        version_bot=self.bot.version
        version_guia=self.bot.guias[str(ctx.guild.id)]["version"]
        prefijo=ctx.prefix

        info_ui = InfoUI(version_bot=version_bot, version_guia=version_guia, prefijo=prefijo)
        opciones_iniciales = cargar_json(INFO_MESSAGE)
        opciones_iniciales["campos"] = dict(list(opciones_iniciales["campos"].items())[:6])

        formatos = {"version_bot": version_bot,
                    "version_guia": version_guia,
                    "prefijo": prefijo}

        embed = Embebido(opciones=opciones_iniciales,
                         formatos=formatos)

        mensaje = USER_CONSULT.format(mencion=ctx.author.mention)

        if "-dm" in opciones:

            await mandar_dm(ctx,
                            contenido=mensaje,
                            vista=info_ui, embed=embed)

        else:

            await ctx.channel.send(content=mensaje,
                                   view=info_ui, embed=embed)


    @command(name="version",
             aliases=["ver"],
             usage="[-dm]",
             help="Muestra la versión del bot.")
    async def mostrar_version(self, ctx: Context, *opciones) -> None:
        """
        Muestra en el chat la versión actual del bot.
        """

        mensaje = f"Mi versión actual es la `{self.bot.version}`"

        if "-dm" in opciones:

            await mandar_dm(ctx, mensaje)

        else:

            await ctx.channel.send(mensaje)

    @command(name="whatsnew",
             aliases=["quehaydenuevo", "nuevo"],
             help="Muestra las novedades de la versión actual.",
             hidden=True)
    async def mostrar_novedades(self, ctx: Context):
        """
        Muestra las novedades de la versión más nueva del bot.
        """

        await ctx.channel.send(content=WHATSNEW, delete_after=60)


    @command(name="test")
    async def prueba(self, ctx: Context, num: str='1', ej: str='1'):

        guia = cargar_json(f"guia/2c2019_exp/guia_{num}.json")

        ejercicio = guia[ej]

        if not ejercicio["titulo"]:

            ejercicio["titulo"] = [f"**Unidad** {num} - \"{guia['titulo']}\" | **Ejercicio** {ej}"]

        embebido = Embebido(opciones=ejercicio)
        mensaje = USER_CONSULT.format(mencion=ctx.author.mention)

        await ctx.channel.send(content=mensaje, embed=embebido)
