"""
Módulo dedicado a contener las UIs de mensajes.
"""

from typing import Optional
from random import choice

from discord import Interaction, Message, PartialEmoji as Emoji, SelectOption
from discord.ui import View, Button, button, Select, select
from discord.enums import ButtonStyle

import archivos
import ppt
from constantes import MESSAGE_FORMAT, REPO_URL, PREFIXES_PATH, DEFAULT_PREFIX, BOT_VERSION, DEFAULT_VERSION, INFO_MESSAGE


class InfoUI(View):
    """
    Clase de una UI personalizada para el mensaje de INFO.
    """

    def __init__(self, ui_timeout: Optional[float]=120.0) -> None:
        """
        Crea una instancia de 'InfoUI'.
        """

        super().__init__(timeout=ui_timeout)

        self.pagina = 1
        self.max_paginas = 2

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

        prefijo = archivos.cargar_valor(PREFIXES_PATH, str(interaccion.message.guild.id), DEFAULT_PREFIX)

        nuevo_contenido = INFO_MESSAGE[f"{self.pagina}"].format(prefix=prefijo, version=DEFAULT_VERSION, version_bot=BOT_VERSION)

        return await interaccion.response.edit_message(content=nuevo_contenido, view=self)


    @button(style=ButtonStyle.grey, custom_id="pg_left", emoji=Emoji.from_str("\N{Leftwards Black Arrow}"), disabled=True)
    async def pagina_anterior(self, boton: Button, interaccion: Interaction) -> None:
        """
        Se intenta ir a la página anterior del mensaje INFO.
        """

        self.pagina -= 1

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey, custom_id="pg_right", emoji=Emoji.from_str("\N{Black Rightwards Arrow}"), disabled=False)
    async def pagina_posterior(self, boton: Button, interaccion: Interaction) -> None:
        """
        Se intenta ir a la página posterior del mensaje INFO.
        """

        self.pagina += 1

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


class SelectorGuia(View):
    """
    Clase de una UI personalizada para cambiar de guías.
    """

    def __init__(self, version_actual: Optional[str]=None, ui_timeout: Optional[float]=120.0) -> None:
        """
        Crea una instancia de 'InfoUI'.
        """

        super().__init__(timeout=ui_timeout)

        self.version_actual = version_actual


    @select(placeholder="Seleccione una versión de la guía", custom_id="selector_de_guia", options=[SelectOption(label=ver) for ver in archivos.lista_versiones()], max_values=1)
    async def seleccionar_guia(self, seleccion: Select, interaccion: Interaction) -> None:
        """
        Muestra y selecciona una versión específica de la guía.
        """

        version_vieja = self.version_actual
        nueva_version = seleccion.values[0] # Debería tener sólo un elemento
        self.version_actual = nueva_version
        
        archivos.actualizar_guia(nueva_version, str(interaccion.message.guild.id))

        await interaccion.response.edit_message(content=f"**[AVISO]** La versión de la guía fue cambiada{f' de `{version_vieja}`' if version_vieja else ''} a `{nueva_version}` exitosamente.", view=None)


class MenuSelectorUnidad(Select):
    """
    Clase que representa un menú selector de Unidades, no la interfaz en sí.
    """

    def __init__(
        self,
        *,
        custom_id: str="menu_selector_unidad",
        placeholder: Optional[str]="Seleccione una Unidad",
        min_values: int=1,
        max_values: int=1,
        disabled: bool=False,
        row: Optional[int]=None,
        guia: archivos.DiccionarioGuia=archivos.cargar_guia(DEFAULT_VERSION)
    ) -> None:
        """
        Crea una instacia de 'MenuSelectorUnidad'.
        """

        self.guia = guia

        opciones = [SelectOption(label=f"Unidad {unidad}", value=unidad, description=self.guia[unidad]["titulo"]) for unidad in archivos.lista_unidades(self.guia)]

        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=opciones, disabled=disabled, row=row)


    async def callback(self, interaccion: Interaction) -> None:
        """
        Procesa la unidad elegida por el usuario del menú selector.
        """

        unidad_elegida = self.values[0]

        await interaccion.response.edit_message(content="Elija el ejercicio", view=SelectorEjercicios(guia=self.guia, unidad=unidad_elegida))


class SelectorUnidad(View):
    """
    Clase de una UI personalizada para seleccionar unidades
    de ejercicios.
    """

    def __init__(self, guia: archivos.DiccionarioGuia, ui_timeout: Optional[float]=120.0) -> None:
        """
        Crea una instancia de 'SelectorUnidad'.
        """

        super().__init__(timeout=ui_timeout)

        self.add_item(MenuSelectorUnidad(guia=guia))


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
        guia: archivos.DiccionarioGuia=archivos.cargar_guia(DEFAULT_VERSION),
        unidad: Optional[archivos.DiccionarioPares]=None
    ) -> None:
        """
        Crea una instacia de 'MenuSelectorEjercicio'.
        """

        self.guia = guia

        if not unidad:

            unidad = archivos.lista_unidades(self.guia)[0]

        self.unidad = unidad

        opciones = [SelectOption(label=f"Ejercicio {ejercicio}", value=ejercicio) for ejercicio in archivos.lista_ejercicios(self.guia, unidad)]

        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=opciones, disabled=disabled, row=row)


    async def callback(self, interaccion: Interaction) -> None:
        """
        Procesa el ejercicio elegido por el usuario del menú selector.
        """

        ejercicio = self.values[0]
        enunciado = self.guia[self.unidad][ejercicio]

        mensaje = MESSAGE_FORMAT.format(mention=interaccion.user.mention, unidad=self.unidad, titulo=self.guia[self.unidad]["titulo"], ejercicio=ejercicio, enunciado=enunciado)

        interfaz = NavegadorEjercicios(guia=self.guia, unidad=self.unidad, ejercicio=ejercicio)

        await interaccion.response.edit_message(content=mensaje, view=interfaz)


class SelectorEjercicios(View):
    """
    Clase de uan UI personalizada para seleccionar ejercicios.
    """

    def __init__(self, guia: archivos.DiccionarioGuia, unidad: archivos.DiccionarioPares, ui_timeout: Optional[float]=120.0) -> None:
        """
        Crea uan instancia de 'SelectorEjercicios'.
        """

        super().__init__(timeout=ui_timeout)

        self.add_item(MenuSelectorEjercicio(guia=guia, unidad=unidad))


class NavegadorEjercicios(View):
    """
    Clase para navegar por los ejercicios de la guía.
    """

    def __init__(self, guia: archivos.DiccionarioGuia, unidad: archivos.DiccionarioPares, ejercicio: str, ui_timeout: Optional[float]=120.0) -> None:
        """
        Crea una instancia de 'NavegadorEjercicios'.
        """

        super().__init__(timeout=ui_timeout)

        self.guia = guia
        self.unidad_actual = unidad
        self.ejercicio_actual = ejercicio

        self.ejercicios = None
        self.max_ejercicios = None
        self.actualizar_ejercicios()

        self.unidades = archivos.lista_unidades(self.guia)
        self.max_unidades = len(self.unidades)

        self.actualizar_botones()


    def get_enunciado(self) -> str:
        """
        Va a buscar el enunciado del ejercicio especificado.
        """

        return self.guia[self.unidad_actual][self.ejercicio_actual]

    def get_mensaje_enunciado(self, mencion_autor: str) -> str:
        """
        Formatea el mensaje del enunciado con lso datos del objeto.
        """

        return MESSAGE_FORMAT.format(mention=mencion_autor,
                                     unidad=self.unidad_actual,
                                     titulo=self.guia[self.unidad_actual]["titulo"],
                                     ejercicio=self.ejercicio_actual,
                                     enunciado=self.get_enunciado())


    def actualizar_ejercicios(self) -> None:
        """
        Actualiza la lista de ejercicios conforme a la
        unidad actual.
        """

        self.ejercicios = archivos.lista_ejercicios(self.guia, self.unidad_actual)
        self.max_ejercicios = len(self.ejercicios)


    def actualizar_boton(self, boton: Button) -> Button:
        """
        Muestra u oculta el botón dependiendo de qué ejercicio sea.
        """

        if any(((boton.custom_id == "u_left" and self.unidad_actual == self.unidades[0]),
               (boton.custom_id == "ex_left" and self.ejercicio_actual == self.ejercicios[0]),
               (boton.custom_id == "ex_right" and self.ejercicio_actual == str(self.max_ejercicios)),
               (boton.custom_id == "u_right") and self.unidad_actual == str(self.max_unidades))):

            boton.disabled = True

        else:

            boton.disabled = False


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

        contenido_mensaje = self.get_mensaje_enunciado(mencion_autor=interaccion.user.mention)

        await interaccion.response.edit_message(content=contenido_mensaje, view=self)


    @button(style=ButtonStyle.grey, custom_id="u_left", emoji=Emoji.from_str("\N{Black Left-Pointing Double Triangle}"))
    async def unidad_anterior(self, boton: Button, interaccion: Interaction) -> None:
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


    @button(style=ButtonStyle.grey, custom_id="ex_left", emoji=Emoji.from_str("\N{Leftwards Black Arrow}"))
    async def ejercicio_anterior(self, boton: Button, interaccion: Interaction) -> None:
        """
        Se intenta ir a la página anterior del mensaje INFO.
        """

        self.ejercicio_actual = int(self.ejercicio_actual)
        self.ejercicio_actual -= 1
        self.ejercicio_actual = str(self.ejercicio_actual)

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey, custom_id="ex_right", emoji=Emoji.from_str("\N{Black Rightwards Arrow}"))
    async def ejercicio_posterior(self, boton: Button, interaccion: Interaction) -> None:
        """
        Se intenta ir a la página posterior del mensaje INFO.
        """

        self.ejercicio_actual = int(self.ejercicio_actual)
        self.ejercicio_actual += 1
        self.ejercicio_actual = str(self.ejercicio_actual)

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


    @button(style=ButtonStyle.grey, custom_id="u_right", emoji=Emoji.from_str("\N{Black Right-Pointing Double Triangle}"))
    async def unidad_posterior(self, boton: Button, interaccion: Interaction) -> None:
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


    @button(style=ButtonStyle.grey, custom_id="ex_random", emoji=Emoji.from_str("\N{Anticlockwise Downwards and Upwards Open Circle Arrows}"))
    async def ejercicio_aleatorio(self, boton: Button, interaccion: Interaction) -> None:
        """
        Muestra un ejercicio completamente aleatorio de toda
        la guía.
        """

        self.unidad_actual = choice(self.unidades)
        self.actualizar_ejercicios()
        self.ejercicio = choice(self.ejercicios)

        self.actualizar_botones()

        await self.actualizar_mensaje(interaccion)


class JuegoPPT(View):
    """
    Interfaz con la que jugar Piedra, Papel, o Tijeras.
    """

    def __init__(self, stats: archivos.DiccionarioStats, ui_timeout: Optional[float]=120.0) -> None:
        """
        Crea uan instancia de 'JuegoPPT'.
        """

        super().__init__(timeout=ui_timeout)

        self.stats_juego = stats

    @button(style=ButtonStyle.blurple, custom_id="rock", label="Piedra", emoji=Emoji.from_str("\N{rock}"))
    async def elegir_piedra(self, boton: Button, interaccion: Interaction) -> None:
        """
        El usuario ha elegido 'Piedra' en una partida de 'Piedra, Papel o Tijeras'.
        """

        await ppt.jugar_partida_ppt("PIEDRA", str(interaccion.user.id), interaccion.message, self.stats_juego)

    @button(style=ButtonStyle.blurple, custom_id="paper", label="Papel", emoji=Emoji.from_str("\N{roll of paper}"))
    async def elegir_papel(self, boton: Button, interaccion: Interaction) -> None:
        """
        El usuario ha elegido 'Piedra' en una partida de 'Piedra, Papel o Tijeras'.
        """

        await ppt.jugar_partida_ppt("PAPEL", str(interaccion.user.id), interaccion.message, self.stats_juego)

    @button(style=ButtonStyle.blurple, custom_id="scissors", label="Tijeras", emoji=Emoji.from_str("\N{Black Scissors}"))
    async def elegir_tijeras(self, boton: Button, interaccion: Interaction) -> None:
        """
        El usuario ha elegido 'Piedra' en una partida de 'Piedra, Papel o Tijeras'.
        """

        await ppt.jugar_partida_ppt("TIJERAS", str(interaccion.user.id), interaccion.message, self.stats_juego)
