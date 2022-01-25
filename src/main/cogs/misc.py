"""
Cog para comandos misceláneos o de consultas.
"""

from discord.ext.commands import Context, command

from ..archivos.archivos import cargar_json
from ..auxiliar.auxiliar import mandar_dm
from ..constantes.constantes import INFO_MESSAGE, WHATSNEW
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
        opciones_iniciales["campos"] = opciones_iniciales["campos"][:6]

        formatos = {"version_bot": version_bot,
                    "version_guia": version_guia,
                    "prefijo": prefijo}

        embed = Embebido(formatos=formatos,
                         opciones=opciones_iniciales)

        if "-dm" in opciones:

            await mandar_dm(ctx,
                            contenido=f"{ctx.author.mention} ha consultado:",
                            vista=info_ui, embed=embed)

        else:

            await ctx.channel.send(content=f"{ctx.author.mention} ha consultado:",
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
