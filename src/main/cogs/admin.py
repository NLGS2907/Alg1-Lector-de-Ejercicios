"""
Cog para comandos que requieren permisos especiales.
"""

from discord.ext.commands import command, Context, check, is_owner

from ..auxiliar.auxiliar import es_rol_valido
from ..constantes.constantes import LOG_PATH, PROPERTIES_PATH
from ..logger.logger import log
from ..archivos.archivos import cargar_json, guardar_json
from .general import CogGeneral


class CogAdmin(CogGeneral):
    """
    Cog de comandos que requieren permisos.
    """

    @command(name="prefix", aliases=["prefijo", "pfx", "px"], usage="<nuevo_prefijo>", help="Cambia el prefijo de los comandos.")
    @check(es_rol_valido)
    async def cambiar_prefijo(self, ctx: Context, nuevo_prefijo: str) -> None:
        """
        Cambia el prefijo utilizado para convocar a los comandos, solamente del
        servidor de donde el comando fue escrito.

        Se da por hecho que el servidor ya está memorizado en el diccionario.
        """

        prefijo_viejo = ctx.prefix

        propiedades = cargar_json(PROPERTIES_PATH)
        propiedades["prefijos"][str(ctx.guild.id)] = nuevo_prefijo
        guardar_json(propiedades, PROPERTIES_PATH)

        await ctx.channel.send(f"**[AVISO]** El prefijo de los comandos fue cambiado de `{prefijo_viejo}` a `{nuevo_prefijo}` exitosamente.", delete_after=30)
        log.info(f"El prefijo de comandos en '{ctx.guild.name}' fue cambiado de '{prefijo_viejo}' a '{nuevo_prefijo}'")


    @command(name="clear", aliases=["clean", "cls"], usage="<limite> | -full", help="Limpia el canal de mensajes del bot.")
    @check(es_rol_valido)
    async def limpiar_mensajes(self, ctx: Context, limite: int=10, *opciones) -> None:
        """
        Limpia los mensajes del bot del canal de donde se
        invoca el comando.

        Si 'full' está entre las opciones, también borra los
        mensajes de los usuarios que invocan los comandos.
        """

        funcion_check = (self.bot.es_mensaje_comando if "-full" in opciones else self.bot.es_mensaje_de_bot)
        eliminados = await ctx.channel.purge(limit=limite + 1, check=funcion_check)

        log.info(f"{len(eliminados)} mensajes fueron eliminados de '#{ctx.channel.name}' en '{ctx.guild.name}'")


    @command(name="shutdown", aliases=["shut", "exit", "quit", "salir"], help="Apaga el bot. Uso exclusivo del dev.", hidden=True)
    @is_owner()
    async def shutdown(self, ctx: Context) -> None:
        """
        Apaga el bot y lo desconecta.
        """

        log.info(f"Cerrando Bot...")
        await ctx.message.delete()
        await ctx.bot.close()


    @command(name="flush", aliases=["logclear"], help="Vacía el archivo de registro. Uso exclusivo del dev.", hidden=True)
    @is_owner()
    async def logflush(self, ctx: Context):
        """
        Vacía el contenido del archivo de registro.
        """

        with open(LOG_PATH, mode='w'):

            await ctx.channel.send(f"**[AVISO]** Vaciando archivo en `./{LOG_PATH}`...", delete_after=10)