"""
Módulo para contener Embeds personalizados.
"""

from discord import Colour, Embed


class Embebido(Embed):
    """
    Clase de embebido personalizada.
    """

    def __init__(self,
                 *,
                 opciones,
                 formatos: dict[str, str]=None) -> None:
        """
        Inicializa una instancia de 'Embebido'.
        """

        self.formatos = {} if formatos is None else formatos

        titulo: list[str] = opciones.get("titulo", [])
        descripcion: list[str] = opciones.get("descripcion", [])
        color: int = opciones.get("color", Colour.dark_grey())
        campos: dict[str, list[str]] = opciones.get("campos", {})
        pie: list[str] = opciones.get("pie", [])

        super().__init__(title=self.custom_format(Embebido.unir(titulo)),
                         description=self.custom_format(Embebido.unir(descripcion)),
                         colour=color)

        for nombre, valores in campos.items():

            self.add_field(name=self.custom_format(nombre),
                           value=self.custom_format(Embebido.unir(valores)),
                           inline=False)

        self.set_footer(text=self.custom_format(Embebido.unir(pie)))


    @staticmethod
    def unir(lista: list[str]) -> str:
        """
        Une los strings de una lista con nuevas líneas.
        """

        return '\n'.join(lista) if lista else ''

    def custom_format(self, cadena: str) -> str:
        """
        Formatea una cadena de manera personalizada.
        """

        for clave, valor in self.formatos.items():

            cadena = cadena.replace('{' + clave + '}', valor)

        return cadena
