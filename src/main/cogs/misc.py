"""
Cog para comandos misceláneos o de consultas.
"""

from discord.ext.commands import Context, command

from ..archivos.archivos import cargar_json
from ..auxiliar.auxiliar import mandar_dm
from ..constantes.constantes import INFO_MESSAGE, USER_CONSULT, WHATSNEW_MESSAGE
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

        contenido = USER_CONSULT.format(mencion=ctx.author.mention)

        if "-dm" in opciones:

            await mandar_dm(ctx,
                            contenido=contenido,
                            vista=info_ui, embed=embed)

        else:

            mensaje_enviado = await ctx.channel.send(content=contenido,
                                   view=info_ui, embed=embed)
            info_ui.msg = mensaje_enviado


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

        await ctx.message.delete(delay=5.0)

    @command(name="whatsnew",
             aliases=["quehaydenuevo", "nuevo"],
             help="Muestra las novedades de la versión actual.",
             hidden=True)
    async def mostrar_novedades(self, ctx: Context):
        """
        Muestra las novedades de la versión más nueva del bot.
        """

        opciones = cargar_json(WHATSNEW_MESSAGE)
        formatos = {"version_bot": self.bot.version}

        embebido = Embebido(opciones=opciones, formatos=formatos)

        await ctx.message.delete(delay=5.0)
        await ctx.channel.send(embed=embebido, delete_after=30.0)
