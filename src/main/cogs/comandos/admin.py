"""
Cog para comandos que requieren permisos especiales.
"""

from os import execl
from sys import executable as sys_executable
from typing import TYPE_CHECKING

from discord import Interaction
from discord.app_commands import Choice, choices
from discord.app_commands import command as appcommand
from discord.app_commands import describe

from ...auxiliar import es_rol_valido
from ...db.atajos import actualizar_prefijo, get_prefijo_guild, get_ruta_log
from ..general import CogGeneral

if TYPE_CHECKING:
    from ...lector import Lector


class CogAdmin(CogGeneral):
    """
    Cog de comandos que requieren permisos.
    """

    @appcommand(name="prefix",
                description="Cambia el prefijo de los comandos.")
    @describe(nuevo_prefijo="El nuevo prefijo a usar")
    @es_rol_valido()
    async def cambiar_prefijo(self, interaccion: Interaction, nuevo_prefijo: str) -> None:
        """
        Cambia el prefijo utilizado para convocar a los comandos, solamente del
        servidor de donde el comando fue escrito.

        Se da por hecho que el servidor ya está memorizado en el diccionario.
        """

        prefijo_viejo = get_prefijo_guild(interaccion.guild_id)
        actualizar_prefijo(nuevo_prefijo, interaccion.guild.id)

        await interaccion.response.send_message("**[AVISO]** El prefijo de los comandos fue " +
                                                f"cambiado de `{prefijo_viejo}` a " +
                                                f"`{nuevo_prefijo}` exitosamente.",
                                                ephemeral=True)

        self.bot.log.info(f"El prefijo en '{interaccion.guild.name}' fue cambiado " +
                          f"de '{prefijo_viejo}' a '{nuevo_prefijo}'")


    @appcommand(name="clear",
                description="Limpia el canal de mensajes del bot.")
    @describe(limite="Cuántos mensajes inspeccionar para borrar")
    @choices(completo=[
        Choice(name="Sí", value=1),
        Choice(name="No", value=0)
    ])
    @es_rol_valido()
    async def limpiar_mensajes(self,
                               interaccion: Interaction,
                               limite: int,
                               completo: Choice[int]=1) -> None:
        """
        Limpia los mensajes del bot del canal de donde se
        invoca el comando.

        Si 'completo' es seleccionado, también borra los
        mensajes de los usuarios que invocan los comandos.
        """

        funcion_check = (self.bot.es_mensaje_comando
                         if completo
                         else self.bot.es_mensaje_de_bot)
        eliminados = await interaccion.channel.purge(limit=limite + 1, check=funcion_check)

        mensaje = (f"`{len(eliminados)}` mensaje/s fueron eliminados de " +
                   f"{interaccion.channel.name} en {interaccion.guild.name}")


        await interaccion.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)


    @appcommand(name="shutdown",
                description="Apaga el bot. Uso para moderadores.")
    @es_rol_valido()
    async def shutdown(self, interaccion: Interaction) -> None:
        """
        Apaga el bot y lo desconecta.
        """

        mensaje = f"Cerrando bot **{str(self.bot.user)}...**"

        await interaccion.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)

        await self.bot.close()


    @appcommand(name="reboot",
                description="Reinicia el bot. Uso para moderadores.")
    @es_rol_valido()
    async def reboot(self, interaccion: Interaction) -> None:
        """
        Reinicia el bot, apagándolo y volviéndolo a conectar.
        """

        if not sys_executable:

            mensaje = "[ERROR] No se pudo reiniciar el lector."

            await interaccion.response.send_message(content=mensaje,
                                                    ephemeral=True)
            self.bot.log.error(mensaje)
            return

        mensaje = f"Reiniciando bot **{str(self.bot.user)}...**"

        await interaccion.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)

        execl(sys_executable, sys_executable, "-m", "src.main.main")


    @appcommand(name="flush",
                description="Vacía el archivo de registro. Uso para moderadores.")
    @es_rol_valido()
    async def logflush(self, interaccion: Interaction):
        """
        Vacía el contenido del archivo de registro.
        """

        ruta_log = get_ruta_log()

        with open(ruta_log, mode='w', encoding="utf-8"):
            await interaccion.response.send_message("**[AVISO]** Vaciando archivo en " +
                                                    f"`./{ruta_log}`...",
                                                    ephemeral=True)


    @appcommand(name="uptime",
                description="Calcula el tiempo que el bot estuvo activo.")
    @es_rol_valido()
    async def calcular_uptime(self, interaccion: Interaction) -> None:
        """
        Calcula el tiempo que el bot estuvo corriendo.
        """

        delta = self.bot.uptime

        dias = (f"`{delta.days}` día/s" if delta.days > 9 else "")

        horas_posibles = (delta.seconds // 3600)
        horas = (f"`{horas_posibles}` hora/s" if horas_posibles > 0 else "")

        minutos_posibles = ((delta.seconds % 3600) // 60)
        minutos = (f"`{minutos_posibles}` minuto/s" if minutos_posibles > 0 else "")

        segundos_posibles = (delta.seconds % 60)
        segundos = (f"`{segundos_posibles}` segundo/s" if segundos_posibles > 0 else "")

        tiempo = [tmp for tmp in [dias, horas, minutos, segundos] if tmp]
        if len(tiempo) > 1:
            ultimo = tiempo.pop()
            tiempo[-1] = f"{tiempo[-1]} y {ultimo}"


        await interaccion.response.send_message(f"***{self.bot.user}** estuvo activo por " +
                                                f"{', '.join(tiempo)}.*",
                                                ephemeral=True)


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogAdmin(bot))
