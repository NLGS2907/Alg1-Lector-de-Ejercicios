"""
Cog para comandos misceláneos o de consultas.
"""

from typing import TYPE_CHECKING

from discord import Interaction, Permissions
from discord.app_commands import command as appcommand
from discord.utils import oauth_url

from ..archivos import cargar_json
from ..constantes import WHATSNEW_MESSAGE
from ..embebido import Embebido
from .general import CogGeneral

if TYPE_CHECKING:

    from ..lector import Lector


class CogMisc(CogGeneral):
    """
    Cog para comandos misceláneos.
    """

    @appcommand(name="version",
                description="Muestra la versión del bot.")
    async def mostrar_version(self, interaction: Interaction) -> None:
        """
        Muestra en el chat la versión actual del bot.
        """

        await interaction.response.send_message(f"Mi versión actual es la `{self.bot.version}`",
                                                ephemeral=True)


    @appcommand(name="whatsnew",
                description="Muestra las novedades de la versión actual.")
    async def mostrar_novedades(self, interaction: Interaction) -> None:
        """
        Muestra las novedades de la versión más nueva del bot.
        """

        opciones = cargar_json(WHATSNEW_MESSAGE)
        formatos = {"version_bot": self.bot.version}

        embebido = Embebido(opciones=opciones, formatos=formatos)

        await interaction.response.send_message(embed=embebido)


    @appcommand(name="invite",
                description="Muestra el link de invitación del lector.")
    async def invitar_bot(self, interaction: Interaction) -> None:
        """
        Manda un mensaje indicando cuál es el enlace de invitación del lector.
        """

        link = oauth_url(self.bot.application_id,
                         permissions=Permissions(permissions=19327560768))

        await interaction.response.send_message(f"Mi enlace de invitación es:\n\n{link}\n\n" +
                                                "*!Sino igual puedes apretar el botón " +
                                                "que hay en mi perfil!*",
                                                ephemeral=True)


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogMisc(bot))
