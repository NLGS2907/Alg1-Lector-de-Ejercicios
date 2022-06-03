"""
Cog para comandos del ahorcado.
"""

from typing import TYPE_CHECKING, Optional

from discord import Interaction
from discord.app_commands import command as appcommand
from discord.app_commands.errors import AppCommandError, CheckFailure

from ..auxiliar import es_hilo
from .general import CogGeneral

if TYPE_CHECKING:

    from ..lector import Lector


class CogHanged(CogGeneral):
    """
    Cog para comandos relacionados al ahorcado.
    """

    async def comando_afuera_de_hilo(self,
                                     interaction: Interaction,
                                     error: AppCommandError) -> None:
        """
        Un comando de dentro de un hilo fue llamado fuera.
        """

        if isinstance(error, CheckFailure):
            nombre_comando = (f" `{interaction.command.name}`" if interaction.command else '')
            contenido = (f"**[ERROR]** El comando{nombre_comando} sólo puede ser utilizado " +
                         "dentro de una partida de ahorcado.")
            await interaction.response.send_message(content=contenido,
                                                    ephemeral=True)

    @appcommand(name="hanged",
                description="Interactúa con un juego de ahorcado.")
    async def crear_sala(self,
                         interaction: Interaction,
                         frase: Optional[str]=None,
                         vidas: int=7) -> None:
        """
        Dependiendo de los comandos que se pasen, interactúa con
        las de juego de ahorcado que hay actualmente.
        """

        await self.bot.hanged_create(interaction, frase, vidas)


    @appcommand(name="guess",
                description="Comando para adivinar una letra en el comando.")
    @es_hilo()
    async def adivinar_letra(self, interaction: Interaction, letra: str) -> None:
        """
        Adivina una letra en una partida en curso de ahorcado.
        """

        await self.bot.hanged_guess(interaction, letra)

        termino, es_victoria = self.bot.partidas[str(interaction.channel.id)].termino_juego()

        if termino:
            await self.bot.fin_del_juego(interaction, es_victoria)


    @adivinar_letra.error
    async def adivina_afuera_de_hilo(self,
                                     interaction: Interaction,
                                     error: AppCommandError) -> None:
        """
        El usuario intenta adivinar una letra de una partida que no existe.
        """

        await self.comando_afuera_de_hilo(interaction, error)


    @appcommand(name="display",
                description="Muestra la pantalla del juego de ahorcado, " +
                            "por si es muy molesto scrollear.")
    @es_hilo()
    async def mostrar_juego(self, interaction: Interaction) -> None:
        """
        Muestra el estado actual de un juego de ahorcado, si
        de tantos mensajes es molesto ver la pantalla ya.
        """

        partida = self.bot.encontrar_partida(str(interaction.channel.id))

        if not partida:
            return

        nuevo_display = await interaction.channel.send(str(partida))
        partida.definir_display(nuevo_display.id)

        await interaction.response.send_message(content="Display Cambiado.",
                                                ephemeral=True)


    @mostrar_juego.error
    async def mostar_pantalla_afuera_de_hilo(self,
                                             interaction: Interaction,
                                             error: AppCommandError) -> None:
        """
        El usuario está tratando de actualizar la pantalla de ahorcado,
        fuera de una partida de ahorcado.
        """

        await self.comando_afuera_de_hilo(interaction, error)


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogHanged(bot))
