"""
Cog para escuchar eventos del Bot.
"""

from typing import TYPE_CHECKING

from discord import Guild, Thread
from discord.ext.commands import Cog, Context

from ...db.atajos import actualizar_guild
from ..general import CogGeneral

if TYPE_CHECKING:
    from ...lector import Lector


class CogEventos(CogGeneral):
    """
    Cog que escucha eventos.
    """

    @Cog.listener()
    async def on_ready(self) -> None:
        """
        El bot se conectó y está listo para usarse.
        """

        self.bot.log.info("Actualizando base de datos...")
        self.bot.actualizar_db()

        self.bot.log.info("¡%s conectado y listo para utilizarse!", self.bot.user)


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

        self.bot.log.info("El usuario %(autor)s está tratando de invocar '%(cmd)s' " % formato_log +
                          "en el canal '#%(canal)s' del server '%(guild)s' " % formato_log +
                          "mediante el mensaje '%(msg)s'" % formato_log)

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        """
        El usuario ejecutó el comando satisfactoriamente.
        """

        formato_log = {"autor": ctx.author,
                       "cmd": ctx.command}

        self.bot.log.info("%(autor)s ha invocado '%(cmd)s' satisfactoriamente", formato_log)


    @Cog.listener()
    async def on_guild_join(self, guild: Guild) -> None:
        """
        El bot se conectó por primera vez a un servidor.
        """

        self.bot.log.info("El bot se conectó a '%s'", guild.name)
        actualizar_guild(guild.id, guild.name)



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

            self.bot.log.info("Partida '%(nombre)s' archivada en '%(guild)s'", formato_log)
            await after.parent.send(content=f"**[AVISO]** Partida `{after.name}` fue " +
                                    "eliminada al ser archivado (probablemente por la hora " +
                                    "de inactividad).",
                                    delete_after=5.0)
            if after.starter_message:
                await after.starter_message.delete()
            await after.delete()


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogEventos(bot))
