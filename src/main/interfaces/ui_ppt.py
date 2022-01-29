"""
Interfaz para un juego de \"Piedras, Papel o Tijeras\".
"""

from discord import Interaction
from discord import PartialEmoji as Emoji
from discord.enums import ButtonStyle
from discord.ui import Button, button

from ..archivos.archivos import DiccionarioStats
from ..ppt.ppt import jugar_partida_ppt
from .ui_general import VistaGeneral


class JuegoPPT(VistaGeneral):
    """
    Interfaz con la que jugar Piedra, Papel, o Tijeras.
    """

    def __init__(self, stats: DiccionarioStats) -> None:
        """
        Crea uan instancia de 'JuegoPPT'.
        """

        super().__init__()
        self.stats_juego = stats

    @button(style=ButtonStyle.blurple,
            custom_id="rock",
            label="Piedra",
            emoji=Emoji.from_str("\N{rock}"))
    async def elegir_piedra(self, _boton: Button, interaccion: Interaction) -> None:
        """
        El usuario ha elegido 'Piedra' en una partida de 'Piedra, Papel o Tijeras'.
        """

        await jugar_partida_ppt("PIEDRA",
                                str(interaccion.user.id),
                                interaccion.message,
                                self.stats_juego)

    @button(style=ButtonStyle.blurple,
            custom_id="paper",
            label="Papel",
            emoji=Emoji.from_str("\N{roll of paper}"))
    async def elegir_papel(self, _boton: Button, interaccion: Interaction) -> None:
        """
        El usuario ha elegido 'Piedra' en una partida de 'Piedra, Papel o Tijeras'.
        """

        await jugar_partida_ppt("PAPEL",
                                str(interaccion.user.id),
                                interaccion.message,
                                self.stats_juego)

    @button(style=ButtonStyle.blurple,
            custom_id="scissors",
            label="Tijeras",
            emoji=Emoji.from_str("\N{Black Scissors}"))
    async def elegir_tijeras(self, _boton: Button, interaccion: Interaction) -> None:
        """
        El usuario ha elegido 'Piedra' en una partida de 'Piedra, Papel o Tijeras'.
        """

        await jugar_partida_ppt("TIJERAS",
                                str(interaccion.user.id),
                                interaccion.message,
                                self.stats_juego)
