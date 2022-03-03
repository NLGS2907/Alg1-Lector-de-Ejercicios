"""
Cog general para uso de herencia.
"""

from typing import TYPE_CHECKING

from discord.ext.commands import Cog

if TYPE_CHECKING:

    from ..lector import Lector


class CogGeneral(Cog):
    """
    Cog General, para que se herede de él.
    """

    def __init__(self, bot: "Lector") -> None:
        """
        Inicializa una instancia de 'CogGeneral'.
        """

        self.bot: "Lector" = bot
