"""
Interfaz general para el uso de herencia.
"""

from typing import Optional

from discord import Interaction, Message
from discord import PartialEmoji as Emoji
from discord.enums import ButtonStyle
from discord.ui import Button, View

from ..logger import LectorLogger


class BotonCerrar(Button):
    """
    Botón para cerrar la vista actual.
    """

    def __init__(self) -> None:
        "Inicializa una instancia de 'BotonCerrar'."

        super().__init__(style=ButtonStyle.red,
                         custom_id="exit",
                         label="Cerrar",
                         row=2,
                         emoji=Emoji.from_str("\N{Heavy Multiplication X}"))


    async def callback(self, interaccion: Interaction) -> None:
        """
        Cierra la vista actual.
        """

        await interaccion.message.edit(content="*Borrando Mensaje...*",
                                       view=None,
                                       embed=None,
                                       delete_after=3.0)


class VistaGeneral(View):
    """
    Vista general hecha para que se herede de ella.
    """

    def __init__(self,
                 ui_timeout: Optional[float]=120.0,
                 agregar_btn_cerrar: bool=True) -> None:
        """
        Inicializa una instancia de 'VistaGeneral'.
        """

        self._msg: Optional[Message] = None

        super().__init__(timeout=ui_timeout)

        if agregar_btn_cerrar:
            self.add_item(BotonCerrar())


    @property
    def log(self) -> LectorLogger:
        """
        Devuelve el lector de la vista.
        """

        return LectorLogger()


    @property
    def msg(self) -> Message:
        """
        Devuelve el mensaje asociado a esta vista.
        """

        return self._msg


    @msg.setter
    def msg(self, nuevo_msg: Message) -> None:
        """
        Define el mensaje de la vista.
        """

        self._msg = nuevo_msg


    async def on_timeout(self) -> None:
        """
        Deshabilita todos los items, ya que no se
        escuchan más interacciones.
        """

        for item in self.children:
            item.disabled = True

            if item.custom_id == "exit":
                self.remove_item(item)

        self.log.info(f"Vista {self} deshabilitada.")
