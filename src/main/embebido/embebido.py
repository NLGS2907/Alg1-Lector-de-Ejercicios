"""
Módulo para contener Embeds personalizados.
"""

from discord import Colour, Embed

from ..constantes.constantes import (BOT_VERSION, DEFAULT_PREFIX,
                                     DEFAULT_VERSION)


class Embebido(Embed):
    """
    Clase de embebido personalizada.
    """

    def __init__(self,
                 *,
                 formatos: dict[str, str],
                 opciones) -> None:
        """
        Inicializa una instancia de 'Embebido'.
        """

        self.version_bot: str = formatos.get("version_bot", BOT_VERSION)
        self.version_guia: str = formatos.get("version_guia", DEFAULT_VERSION)
        self.prefijo: str = formatos.get("prefijo", DEFAULT_PREFIX)

        titulo: str = opciones.get("titulo", '')
        descripcion: str = opciones.get("descripcion", '')
        color: int = opciones.get("color", Colour.dark_grey())
        campos: list[tuple[str, str]] = opciones.get("campos", [])
        pie: str = opciones.get("pie", '')

        super().__init__(title=self.custom_format(titulo),
                         description=self.custom_format(descripcion),
                         colour=color)

        for nombre, valor in campos:

            self.add_field(name=self.custom_format(nombre),
                           value=self.custom_format(valor),
                           inline=False)

        self.set_footer(text=self.custom_format(pie))


    def custom_format(self, string: str) -> str:
        """
        Formatea un string de una manera personalizada.
        """

        return string.format(version_bot=self.version_bot,
                             version_guia=self.version_guia,
                             prefix=self.prefijo)
