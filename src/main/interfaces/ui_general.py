"""
Interfaz general para el uso de herencia.
"""

from typing import Optional

from discord import Interaction, Message
from discord import PartialEmoji as Emoji
from discord.enums import ButtonStyle
from discord.ui import Button, View

from ..logger.logger import log


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


    async def callback(self, interaction: Interaction) -> None:
        """
        Cierra la vista actual.
        """

        await interaction.message.edit(content="*Borrando Mensaje...*",
                                       view=None,
                                       embed=None,
                                       delete_after=3.0)


class VistaGeneral(View):
    """
    Vista general hecha para que se herede de ella.
    """

    def __init__(self, ui_timeout: Optional[float]=5.0) -> None:
        """
        Inicializa una instancia de 'VistaGeneral'.
        """

        self._msg: Optional[Message] = None

        super().__init__(timeout=ui_timeout)

        self.add_item(BotonCerrar())


    @property
    def msg(self) -> Optional[Message]:
        """
        Accede al mensaje de la vista, si hay uno.
        """

        return self._msg


    @msg.setter
    def msg(self, otro_msg: Message) -> None:
        """
        Reemplaza el mensaje de la vista.
        """

        self._msg = otro_msg


    def limpiar_mensaje(self) -> None:
        """
        Elimina la referencia al mensaje.
        Esto puede ser útil cuando se reemplaza la vista en
        un mensaje por otra distinta.
        """

        self.msg = None


    async def on_timeout(self) -> None:
        """
        Deshabilita todos los items, ya que no se
        escuchan más interacciones.
        """

        if self.msg:

            for item in self.children:

                item.disabled = True

                if item.custom_id == "exit":

                    self.remove_item(item)

            await self.msg.edit(view=self)

        estado_mensaje = ('' if not self.msg
                         else f" en '{self.msg.channel.name}' en el mensaje de id '{self.msg.id}'")
        mensaje_log = f"Vista {self} deshabilitada{estado_mensaje}"
        log.info(mensaje_log)
