"""
Módulo para contener Embeds personalizados.
"""

from discord import Colour, Embed

from ..constantes.constantes import DEFAULT_PREFIX, DEFAULT_VERSION

class Embebido(Embed):
    """
    Clase de embebido personalizada.
    """

    def __init__(self,
                 *,
                 version_bot: str,
                 version_guia: str=DEFAULT_VERSION,
                 prefijo: str=DEFAULT_PREFIX,
                 opciones) -> None:
        """
        Inicializa una instancia de 'Embebido'.
        """

        self.version_bot: str = version_bot
        self.version_guia: str = version_guia
        self.prefijo: str = prefijo

        titulo: str = opciones.get("titulo", '')
        descripcion: str = opciones.get("descripcion", '')
        color: int = opciones.get("color", Colour.dark_grey())
        campos: list[tuple[str, str]] = opciones.get("campos", [])
        pie: str = opciones.get("pie", '')

        super().__init__(title=self.custom_format(titulo), description=self.custom_format(descripcion), colour=color)

        for nombre, valor in campos:

            self.add_field(name=self.custom_format(nombre), value=self.custom_format(valor), inline=False)

        self.set_footer(text=self.custom_format(pie))


    @staticmethod
    def _reemplazar(string: str, substring: str, nuevo_substring: str) -> str:
        """
        Busca si un substring está en el string original.
        Si es el caso, lo reemplaza por uno nuevo.
        Si no, devuelve el mismo string original.
        """

        if substring in string:

            return string.replace(substring, nuevo_substring)

        return string


    def custom_format(self, string: str) -> str:
        """
        Formatea un string de una manera personalizada.
        """

        version_bot = "{version_bot}"
        version_guia = "{version_guia}"
        prefijo = "{prefix}"

        string = Embebido._reemplazar(string, version_bot, self.version_bot)
        string = Embebido._reemplazar(string, version_guia, self.version_guia)
        string = Embebido._reemplazar(string, prefijo, self.prefijo)

        return string