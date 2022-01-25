"""
Cog general para uso de herencia.
"""

from discord.ext.commands import Cog, Bot


class CogGeneral(Cog):
    """
    Cog General, para que se herede de él.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Inicializa una instancia de 'CogGeneral'.
        """

        self.bot: Bot = bot
