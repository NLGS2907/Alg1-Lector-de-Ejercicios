"""
Interfaces para los Ejercicios.
"""

from random import choice
from typing import Optional

from discord import Embed, Interaction, Message
from discord import PartialEmoji as Emoji
from discord import SelectOption
from discord.enums import ButtonStyle
from discord.ui import Button, Select, button

from ...archivos import (DiccionarioEjercicio, DiccionarioGuia,
                         DiccionarioPares, cargar_guia, lista_ejercicios,
                         lista_unidades)
from ...db.atajos import get_guia_default
from ...embebido import Embebido
from ..ui_general import VistaGeneral


USER_CONSULT: str = "**{mencion}** ha consultado:"
TITLE_FORMAT: str = "**Unidad** {unidad} - \"{titulo}\"  |  **Ejercicio** {ejercicio}"


class MenuSelectorEjercicio(Select):
    """
    Clase que representa un menú selector de Ejercicios, no la interfaz en sí.
    """

    def __init__(
        self,
        *,
        custom_id: str="menu_selector_ejercicio",
        placeholder: Optional[str]="Seleccione un Ejercicio",
        min_values: int=1,
        max_values: int=1,
        disabled: bool=False,
        row: Optional[int]=None,
        guia: DiccionarioGuia=cargar_guia(get_guia_default()),
        unidad: Optional[DiccionarioPares]=None
    ) -> None:
        """
        Inicializa una instacia de 'MenuSelectorEjercicio'.
        """

        self.guia = guia

        if not unidad:

            unidad = lista_unidades(self.guia)[0]

        self.unidad = unidad

        opciones = [SelectOption(label=f"Ejercicio {ejercicio}",
                                 description=self.comienzo_enunciado(ejercicio),
                                 value=ejercicio)

                                 for ejercicio in lista_ejercicios(self.guia, unidad)]

        super().__init__(custom_id=custom_id,
                         placeholder=placeholder,
                         min_values=min_values,
                         max_values=max_values,
                         options=opciones,
                         disabled=disabled,
                         row=row)


    def comienzo_enunciado(self, ejercicio: str) -> str:
        """
        Retorna una cadena con los primeros caracteres del enunciado
        de un ejercicio.
        """

        descripcion = self.guia[self.unidad][ejercicio]['descripcion'][0]
        max_char = 50

        return f"{descripcion[:max_char]}{'...' if len(descripcion) > max_char else ''}"

    async def callback(self, interaccion: Interaction) -> None:
        """
        Procesa el ejercicio elegido por el usuario del menú selector.
        """

        ejercicio = self.values[0]
        enunciado = self.guia[self.unidad][ejercicio]

        if not enunciado["titulo"]:

            enunciado["titulo"] = [TITLE_FORMAT.format(unidad=self.unidad,
                                                    titulo=self.guia[self.unidad]["titulo"],
                                                    ejercicio=ejercicio)]

        mensaje = USER_CONSULT.format(mencion=interaccion.user.mention)
        embebido = Embebido(opciones=enunciado)
        vista = NavegadorEjercicios(guia=self.guia, unidad=self.unidad, ejercicio=ejercicio)

        mensaje_editado = await interaccion.response.edit_message(content=mensaje,
                                                                  embed=embebido,
                                                                  view=vista)


class SelectorEjercicios(VistaGeneral):
    """
    Clase de una UI personalizada para seleccionar ejercicios.
    """

    def __init__(self, guia: DiccionarioGuia, unidad: DiccionarioPares) -> None:
        """
        Crea una instancia de 'SelectorEjercicios'.
        """

        super().__init__()
        self.add_item(MenuSelectorEjercicio(guia=guia, unidad=unidad))


class NavegadorEjercicios(VistaGeneral):
    """
    Clase para navegar por los ejercicios de la guía.
    """

    def __init__(self, guia: DiccionarioGuia, unidad: DiccionarioPares, ejercicio: str) -> None:
        """
        Inicializa una instancia de 'NavegadorEjercicios'.
        """

        super().__init__()

        self.guia = guia
        self.unidad_actual = unidad
        self.ejercicio_actual = ejercicio

        self.ejercicios = None
        self.max_ejercicios = None
        self.actualizar_ejercicios()

        self.unidades = lista_unidades(self.guia)

        self.actualizar_botones()


    def get_enunciado(self) -> DiccionarioEjercicio:
        """
        Va a buscar el enunciado del ejercicio especificado.
        """

        enunciado = self.guia[self.unidad_actual][self.ejercicio_actual]

        if not enunciado["titulo"]:

            enunciado["titulo"] = [TITLE_FORMAT.format(unidad=self.unidad_actual,
                                                    titulo=self.guia[self.unidad_actual]["titulo"],
                                                    ejercicio=self.ejercicio_actual)]

        return enunciado


    def get_embebido_enunciado(self) -> Embed:
        """
        Devuelve un embebido con todo el contenido del enunciado.
        """

        return Embebido(opciones=self.get_enunciado())


    def actualizar_ejercicios(self) -> None:
        """
        Actualiza la lista de ejercicios conforme a la
        unidad actual.
        """

        self.ejercicios = lista_ejercicios(self.guia, self.unidad_actual)
        self.max_ejercicios = len(self.ejercicios)


    def actualizar_boton(self, boton: Button) -> Button:
        """
        Muestra u oculta el botón dependiendo de qué ejercicio sea.
        """

        boton.disabled = any(
            (
                (boton.custom_id == "u_left"
                 and self.unidad_actual == self.unidades[0]),
                (boton.custom_id == "ex_left"
                 and self.ejercicio_actual == self.ejercicios[0]),
                (boton.custom_id == "ex_right"
                 and self.ejercicio_actual == str(self.max_ejercicios)),
                (boton.custom_id == "u_right")
                 and self.unidad_actual == str(len(self.unidades))
            )
        )


    def actualizar_botones(self) -> None:
        """
        Cambia y oculta o muestra los botones conforme se cambien
        los ejercicios en muestra.
        """

        self.actualizar_ejercicios()

        for item in self.children:

            if isinstance(item, Button):

                self.actualizar_boton(item)


    async def actualizar_mensaje(self, interaccion: Interaction) -> Message:
        """
        Actualiza el contenido del mensaje especificado.
        Devuelve el mensaje editado.
        """

        contenido_mensaje = USER_CONSULT.format(mencion=interaccion.user.mention)
        embebido = self.get_embebido_enunciado()

        mensaje_editado = await interaccion.response.edit_message(content=contenido_mensaje,
                                                                  embed=embebido,
                                                                  view=self)
        self.msg = mensaje_editado


    @button(style=ButtonStyle.grey,
            custom_id="u_left",
            emoji=Emoji.from_str("\N{Black Left-Pointing Double Triangle}"))
    async def unidad_anterior(self, interaccion: Interaction, _boton: Button) -> None:
        """
        Retrocede hasta el último ejercicio de la unidad anterior.
        """

        self.unidad_actual = int(self.unidad_actual)
        self.unidad_actual -= 1
        self.unidad_actual = str(self.unidad_actual)

        self.actualizar_ejercicios()

        self.ejercicio_actual = self.ejercicios[self.max_ejercicios - 1]

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey,
            custom_id="ex_left",
            emoji=Emoji.from_str("\N{Leftwards Black Arrow}"))
    async def ejercicio_anterior(self, interaccion: Interaction, _boton: Button) -> None:
        """
        Se intenta ir a la página anterior del mensaje INFO.
        """

        self.ejercicio_actual = int(self.ejercicio_actual)
        self.ejercicio_actual -= 1
        self.ejercicio_actual = str(self.ejercicio_actual)

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey,
    custom_id="ex_right",
    emoji=Emoji.from_str("\N{Black Rightwards Arrow}"))
    async def ejercicio_posterior(self, interaccion: Interaction, _boton: Button) -> None:
        """
        Se intenta ir a la página posterior del mensaje INFO.
        """

        self.ejercicio_actual = int(self.ejercicio_actual)
        self.ejercicio_actual += 1
        self.ejercicio_actual = str(self.ejercicio_actual)

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey,
            custom_id="u_right",
            emoji=Emoji.from_str("\N{Black Right-Pointing Double Triangle}"))
    async def unidad_posterior(self, interaccion: Interaction, _boton: Button) -> None:
        """
        Retrocede hasta el primer ejercicio de la unidad siguiente.
        """

        self.unidad_actual = int(self.unidad_actual)
        self.unidad_actual += 1
        self.unidad_actual = str(self.unidad_actual)

        self.actualizar_ejercicios()

        self.ejercicio_actual = self.ejercicios[0]

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey,
            custom_id="ex_random",
            emoji=Emoji.from_str("\N{Anticlockwise Downwards and Upwards Open Circle Arrows}"))
    async def ejercicio_aleatorio(self, interaccion: Interaction, _boton: Button) -> None:
        """
        Muestra un ejercicio completamente aleatorio de toda
        la guía.
        """

        self.unidad_actual = choice(self.unidades)
        self.actualizar_ejercicios()
        self.ejercicio_actual = choice(self.ejercicios)

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)
