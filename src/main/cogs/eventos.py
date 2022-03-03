"""
Cog para escuchar eventos del Bot.
"""

from discord import Guild, Thread
from discord.ext.commands import Cog, Context

from ..archivos import cargar_json, guardar_json
from ..constantes import DEFAULT_PREFIX, DEFAULT_VERSION, PROPERTIES_PATH
from ..logger import log
from .general import CogGeneral


class CogEventos(CogGeneral):
    """
    Cog que escucha eventos.
    """

    @Cog.listener()
    async def on_ready(self) -> None:
        """
        El bot se conectó y está listo para usarse.
        """

        log.info("¡%s conectado y listo para utilizarse!", self.bot.user)

    @Cog.listener()
    async def on_command(self, ctx: Context):
        """
        El usuario está tratando de invocar un comando.
        """

        formato_log = {"autor": ctx.author,
                       "cmd": ctx.command,
                       "canal": ctx.channel.name,
                       "guild": ctx.guild.name,
                       "msg": ctx.message.content}

        log.info("El usuario %(autor)s está tratando de invocar '%(cmd)s' " % formato_log +
                 "en el canal '#%(canal)s' del server '%(guild)s' " % formato_log +
                 "mediante el mensaje '%(msg)s'" % formato_log)

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        """
        El usuario ejecutó el comando satisfactoriamente.
        """

        formato_log = {"autor": ctx.author,
                       "cmd": ctx.command}

        log.info("%(autor)s ha invocado '%(cmd)s' satisfactoriamente", formato_log)


    @Cog.listener()
    async def on_guild_join(self, guild: Guild) -> None:
        """
        El bot se conectó por primera vez a un servidor.
        """

        log.info("El bot se conectó a '%s'", guild.name)

        propiedades = cargar_json(PROPERTIES_PATH)

        propiedades["prefijos"][str(guild.id)] = DEFAULT_PREFIX
        propiedades["versiones_guia"][str(guild.id)] = DEFAULT_VERSION

        guardar_json(propiedades, PROPERTIES_PATH)

        self.bot.guias = self.bot.definir_guias()


    @Cog.listener()
    async def on_thread_update(self, _before: Thread, after: Thread) -> None:
        """
        Un hilo fue actualizado. Si esta actualización fue que el hilo en
        cuestión fue archivado, y si es uno de las partidas de ahorcado,
        lo elimina.
        """

        partida = self.bot.encontrar_partida(str(after.id))

        if partida and after.archived:

            self.bot.partidas.pop(str(after.id))

            formato_log = {"nombre": after.name,
                           "guild": after.guild.name}

            log.info("Partida '%(nombre)s' archivada en '%(guild)s'", formato_log)
            await after.parent.send(content=f"**[AVISO]** Partida `{after.name}` fue " +
                                    "eliminada al ser archivado (probablemente por la hora " +
                                    "de inactividad).")
            await after.delete()
