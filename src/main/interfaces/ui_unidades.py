"""
Interfaz para las Unidades.
"""

from typing import Optional

from discord import Interaction, SelectOption
from discord.ui import Select, select

from ..archivos.archivos import DiccionarioGuia, actualizar_guia, cargar_guia, lista_unidades, lista_carpetas
from .ui_general import VistaGeneral
from .ui_ejercicios import SelectorEjercicios

from ..constantes.constantes import  DEFAULT_VERSION


class SelectorGuia(VistaGeneral):
    """
    Clase de una UI personalizada para cambiar de guías.
    """

    def __init__(self, version_actual: Optional[str]=None) -> None:
        """
        Inicializa una instancia de 'InfoUI'.
        """

        super().__init__()

        self.version_actual = version_actual


    @select(placeholder="Seleccione una versión de la guía", custom_id="selector_de_guia", options=[SelectOption(label=ver) for ver in lista_carpetas()], max_values=1)
    async def seleccionar_guia(self, seleccion: Select, interaccion: Interaction) -> None:
        """
        Muestra y selecciona una versión específica de la guía.
        """

        version_vieja = self.version_actual
        nueva_version = seleccion.values[0] # Debería tener sólo un elemento
        self.version_actual = nueva_version
        
        actualizar_guia(nueva_version, str(interaccion.message.guild.id))

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
        guia: DiccionarioGuia=cargar_guia(DEFAULT_VERSION)
    ) -> None:
        """
        Inicializa una instacia de 'MenuSelectorUnidad'.
        """

        self.guia = guia

        opciones = [SelectOption(label=f"Unidad {unidad}", value=unidad, description=self.guia[unidad]["titulo"]) for unidad in lista_unidades(self.guia)]

        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=opciones, disabled=disabled, row=row)


    async def callback(self, interaccion: Interaction) -> None:
        """
        Procesa la unidad elegida por el usuario del menú selector.
        """

        unidad_elegida = self.values[0]

        await interaccion.response.edit_message(content="Elija el ejercicio", view=SelectorEjercicios(guia=self.guia, unidad=unidad_elegida))


class SelectorUnidad(VistaGeneral):
    """
    Clase de una UI personalizada para seleccionar unidades
    de ejercicios.
    """

    def __init__(self, guia: DiccionarioGuia) -> None:
        """
        Inicializa una instancia de 'SelectorUnidad'.
        """

        super().__init__()

        self.add_item(MenuSelectorUnidad(guia=guia))