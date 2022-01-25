"""
Interfaz general para el uso de herencia.
"""

from typing import Optional

from discord import Interaction
from discord import PartialEmoji as Emoji
from discord.enums import ButtonStyle
from discord.ui import Button, View, button


class VistaGeneral(View):
    """
    Vista general hecha para que se herede de ella.
    """

    def __init__(self, ui_timeout: Optional[float]=120.0) -> None:
        """
        Inicializa una instancia de 'VistaGeneral'.
        """

        super().__init__(timeout=ui_timeout)


    async def on_timeout(self) -> None:
        """
        Deshabilita todos los items, ya que no se
        escuchan más interacciones.
        """

        for item in self.children:

            item.disabled = True

    @button(style=ButtonStyle.red,
            custom_id="exit",
            label="Cerrar",
            row=2,
            emoji=Emoji.from_str("\N{Heavy Multiplication X}"))
    async def cerrar_interfaz(self, _: Button, interaccion: Interaction) -> None:
        """
        Cierra la interfaz actual.
        """

        await interaccion.message.edit(content="*Borrando Mensaje...*",
                                       view=None,
                                       embed=None,
                                       delete_after=3.0)
