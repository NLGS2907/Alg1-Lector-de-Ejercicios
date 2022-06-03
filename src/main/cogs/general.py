"""
Cog general para uso de herencia.
"""

from typing import TYPE_CHECKING, Dict, Tuple

from discord import Message
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
        self.msg_timeouts: Dict[str, Tuple[Message, int]] = {}



async def setup(_bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    ... # Este Cog no está pensado para agregarse.
