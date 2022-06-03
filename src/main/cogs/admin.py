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

from ..archivos import cargar_json, guardar_json
from ..auxiliar import es_rol_valido, get_prefijo_por_id
from ..constantes import LOG_PATH, PROPERTIES_PATH
from .general import CogGeneral

if TYPE_CHECKING:

    from ..lector import Lector


class CogAdmin(CogGeneral):
    """
    Cog de comandos que requieren permisos.
    """

    @appcommand(name="prefix",
                description="Cambia el prefijo de los comandos.")
    @describe(nuevo_prefijo="El nuevo prefijo a usar")
    @es_rol_valido()
    async def cambiar_prefijo(self, interaction: Interaction, nuevo_prefijo: str) -> None:
        """
        Cambia el prefijo utilizado para convocar a los comandos, solamente del
        servidor de donde el comando fue escrito.

        Se da por hecho que el servidor ya está memorizado en el diccionario.
        """

        prefijo_viejo = get_prefijo_por_id(interaction.guild_id)

        propiedades = cargar_json(PROPERTIES_PATH)
        propiedades["prefijos"][str(interaction.guild.id)] = nuevo_prefijo
        guardar_json(propiedades, PROPERTIES_PATH)

        await interaction.response.send_message("**[AVISO]** El prefijo de los comandos fue " +
                                                f"cambiado de `{prefijo_viejo}` a " +
                                                f"`{nuevo_prefijo}` exitosamente.",
                                                ephemeral=True)

        self.bot.log.info(f"El prefijo en '{interaction.guild.name}' fue cambiado " +
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
                               interaction: Interaction,
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
        eliminados = await interaction.channel.purge(limit=limite + 1, check=funcion_check)

        mensaje = (f"`{len(eliminados)}` mensaje/s fueron eliminados de " +
                   f"{interaction.channel.name} en {interaction.guild.name}")


        await interaction.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)


    @appcommand(name="shutdown",
                description="Apaga el bot. Uso para moderadores.")
    @es_rol_valido()
    async def shutdown(self, interaction: Interaction) -> None:
        """
        Apaga el bot y lo desconecta.
        """

        mensaje = f"Cerrando bot **{str(self.bot.user)}...**"

        await interaction.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)

        await self.bot.close()


    @appcommand(name="reboot",
                description="Reinicia el bot. Uso para moderadores.")
    @es_rol_valido()
    async def reboot(self, interaction: Interaction) -> None:
        """
        Reinicia el bot, apagándolo y volviéndolo a conectar.
        """

        if not sys_executable:

            mensaje = "[ERROR] No se pudo reiniciar el lector."

            await interaction.response.send_message(content=mensaje,
                                                    ephemeral=True)
            self.bot.log.error(mensaje)
            return

        mensaje = f"Reiniciando bot **{str(self.bot.user)}...**"

        await interaction.response.send_message(content=mensaje,
                                                ephemeral=True)
        self.bot.log.info(mensaje)

        execl(sys_executable, sys_executable, "-m", "src.main.main")


    @appcommand(name="flush",
                description="Vacía el archivo de registro. Uso para moderadores.")
    @es_rol_valido()
    async def logflush(self, interaction: Interaction):
        """
        Vacía el contenido del archivo de registro.
        """

        with open(LOG_PATH, mode='w', encoding="utf-8"):
            await interaction.response.send_message("**[AVISO]** Vaciando archivo en " +
                                                    f"`./{LOG_PATH}`...",
                                                    ephemeral=True)


    @appcommand(name="uptime",
                description="Calcula el tiempo que el bot estuvo activo.")
    @es_rol_valido()
    async def calcular_uptime(self, interaction: Interaction) -> None:
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


        await interaction.response.send_message(f"***{self.bot.user}** estuvo activo por " +
                                                f"{', '.join(tiempo)}.*",
                                                ephemeral=True)


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogAdmin(bot))
