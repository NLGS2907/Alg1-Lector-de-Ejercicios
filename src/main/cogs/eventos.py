"""
Cog para escuchar eventos del Bot.
"""

from discord import Guild, Thread
from discord.ext.commands import Cog, Context

from .general import CogGeneral
from ..logger.logger import log
from ..archivos.archivos import cargar_json, guardar_json

from ..constantes.constantes import DEFAULT_PREFIX, DEFAULT_VERSION, PROPERTIES_PATH


class CogEventos(CogGeneral):
    """
    Cog que escucha eventos.
    """

    @Cog.listener()
    async def on_ready(self) -> None:
        """
        El bot se conectó y está listo para usarse.
        """

        log.info(f"¡{self.bot.user} conectado y listo para utilizarse!")

    @Cog.listener()
    async def on_command(self, ctx: Context):
        """
        El usuario está tratando de invocar un comando.
        """

        log.info(f"El usuario {ctx.author} está tratando de invocar '{ctx.command}' en el canal '#{ctx.channel.name}' del server '{ctx.guild.name}' mediante el mensaje '{ctx.message.content}'")

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        """
        El usuario ejecutó el comando satisfactoriamente.
        """

        log.info(f"{ctx.author} ha invocado '{ctx.command}' satisfactoriamente")


    @Cog.listener()
    async def on_guild_join(self, guild: Guild) -> None:
        """
        El bot se conectó por primera vez a un servidor.
        """

        log.info(f"El bot se conectó a '{guild.name}'")

        propiedades = cargar_json(PROPERTIES_PATH)

        propiedades["prefijos"][str(guild.id)] = DEFAULT_PREFIX
        propiedades["versiones_guia"][str(guild.id)] = DEFAULT_VERSION

        guardar_json(propiedades, PROPERTIES_PATH)

        self.bot.guias = self.bot.definir_guias()


    @Cog.listener()
    async def on_thread_update(self, before: Thread, after: Thread) -> None:
        """
        Un hilo fue actualizado. Si esta actualización fue que el hilo en
        cuestión fue archivado, y si es uno de las partidas de ahorcado,
        lo elimina.
        """

        partida = self.bot.encontrar_partida(str(after.id))

        if partida and after.archived:

            self.bot.partidas.pop(str(after.id))
            await after.parent.send(f"**[AVISO]** Partida `{after.name}` fue eliminada al ser archivado (probablemente por la hora de inactividad).")
            await after.delete()