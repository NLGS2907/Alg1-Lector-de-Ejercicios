"""
Módulo para botón de adivinar un ahorcado.
"""

from typing import TYPE_CHECKING

from discord import Interaction
from discord.enums import ButtonStyle
from discord.ui import Button, button

from ..ui_general import VistaGeneral
from .guess_modal import ModalAdivinacion

if TYPE_CHECKING:
    from ...lector import Lector


class VistaAdivinacion(VistaGeneral):
    """
    Vista para adivinar una letra de Ahorcado.
    """

    def __init__(self, bot: "Lector") -> None:
        """
        Inicializa una instancia de 'VistaAdivinacion'.
        """

        super().__init__(agregar_btn_cerrar=False)
        self.bot: "Lector" = bot


    @button(label="Adivinar",
            custom_id="hanged_guess",
            disabled=False,
            style=ButtonStyle.blurple,
            row=0)
    async def adivinar_letra(self, interaccion: Interaction, _boton: Button) -> None:
        """
        Adivina una letra del Ahorcado.
        """

        await interaccion.response.send_modal(ModalAdivinacion(self))
