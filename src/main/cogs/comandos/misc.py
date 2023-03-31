"""
Cog para comandos misceláneos o de consultas.
"""

from typing import TYPE_CHECKING

from discord import Interaction, Permissions
from discord.app_commands import command as appcommand
from discord.utils import oauth_url

from ...db.atajos import get_version
from ..general import CogGeneral

if TYPE_CHECKING:
    from ...lector import Lector


class CogMisc(CogGeneral):
    """
    Cog para comandos misceláneos.
    """

    @appcommand(name="version",
                description="Muestra la versión del bot.")
    async def mostrar_version(self, interaccion: Interaction) -> None:
        """
        Muestra en el chat la versión actual del bot.
        """

        await interaccion.response.send_message(f"Mi versión actual es la `{get_version()}`",
                                                ephemeral=True)


    @appcommand(name="invite",
                description="Muestra el link de invitación del lector.")
    async def invitar_bot(self, interaccion: Interaction) -> None:
        """
        Manda un mensaje indicando cuál es el enlace de invitación del lector.
        """

        link = oauth_url(self.bot.application_id,
                         permissions=Permissions(permissions=19327560768))

        await interaccion.response.send_message(f"Mi enlace de invitación es:\n\n{link}\n\n" +
                                                "*!Sino igual puedes apretar el botón " +
                                                "que hay en mi perfil!*",
                                                ephemeral=True)


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogMisc(bot))
