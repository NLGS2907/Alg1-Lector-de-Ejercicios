"""
Interfaz para el comando 'info'.
"""

from discord import Interaction, Message
from discord import PartialEmoji as Emoji
from discord.enums import ButtonStyle
from discord.ui import Button, button

from ..archivos.archivos import cargar_json
from ..constantes.constantes import (BOT_VERSION, DEFAULT_PREFIX,
                                     DEFAULT_VERSION, INFO_MESSAGE, REPO_URL)
from ..embebido.embebido import Embebido
from .ui_general import VistaGeneral


class InfoUI(VistaGeneral):
    """
    Clase de una UI personalizada para el mensaje de INFO.
    """

    def __init__(self,
                 *,
                 version_bot: str=BOT_VERSION,
                 version_guia: str=DEFAULT_VERSION,
                 prefijo: str=DEFAULT_PREFIX,
                 opciones_embebido=None) -> None:
        """
        Inicializa una instancia de 'InfoUI'.
        """

        super().__init__()

        self.version_bot: str = version_bot
        self.version_guia: str = version_guia
        self.prefijo: str = prefijo
        self.opciones_embebido = (cargar_json(INFO_MESSAGE)
                                  if not opciones_embebido
                                  else opciones_embebido)

        cantidad_campos: int = len(self.opciones_embebido["campos"])
        self.elementos_por_pagina: int = 6

        self.pagina = 1
        self.max_paginas = ((cantidad_campos // self.elementos_por_pagina) +
                            (1 if (cantidad_campos % self.elementos_por_pagina) else 0))

        self.add_item(Button(style=ButtonStyle.grey, label="Repositorio", url=REPO_URL))



    def actualizar_boton(self, boton: Button) -> Button:
        """
        Muestra u oculta el botón dependiendo de qué página sea.
        """

        if any(((boton.custom_id == "pg_left" and self.pagina == 1),
                (boton.custom_id == "pg_right" and self.pagina == self.max_paginas))):

            boton.disabled = True

        else:

            boton.disabled = False

        return boton


    def actualizar_botones(self) -> None:
        """
        Cambia y oculta o muestra los botones conforme se cambian las páginas.
        """

        for item in self.children:

            if isinstance(item, Button):

                self.actualizar_boton(item)


    async def actualizar_mensaje(self, interaccion: Interaction) -> Message:
        """
        Actualiza el contenido del mensaje especificado.
        Devuelve el mensaje editado.
        """

        desde = (self.pagina - 1) * self.elementos_por_pagina
        hasta = self.pagina * self.elementos_por_pagina

        opciones_a_usar = self.opciones_embebido.copy()
        opciones_a_usar["campos"] = dict(list(opciones_a_usar["campos"].items())[desde:hasta])

        formatos = {"version_bot": self.version_bot,
                    "version_guia": self.version_guia,
                    "prefijo": self.prefijo}

        nuevo_embebido = Embebido(opciones=opciones_a_usar,
                                  formatos=formatos)

        mensaje_editado = await interaccion.response.edit_message(embed=nuevo_embebido,
                                                                  view=self)
        self.msg = mensaje_editado

        return mensaje_editado


    @button(style=ButtonStyle.grey,
            custom_id="pg_left",
            emoji=Emoji.from_str("\N{Leftwards Black Arrow}"), disabled=True)
    async def pagina_anterior(self, _boton: Button, interaccion: Interaction) -> None:
        """
        Se intenta ir a la página anterior del mensaje INFO.
        """

        self.pagina -= 1

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey,
            custom_id="pg_right",
            emoji=Emoji.from_str("\N{Black Rightwards Arrow}"), disabled=False)
    async def pagina_posterior(self, _boton: Button, interaccion: Interaction) -> None:
        """
        Se intenta ir a la página posterior del mensaje INFO.
        """

        self.pagina += 1

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)