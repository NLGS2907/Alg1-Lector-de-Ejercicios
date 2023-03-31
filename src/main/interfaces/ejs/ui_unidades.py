"""
Interfaz para las Unidades.
"""

from typing import Optional

from discord import Interaction, SelectOption
from discord.ui import Select, select

from ...archivos import (DiccionarioGuia, cargar_guia, lista_carpetas,
                         lista_unidades)
from ...db.atajos import (actualizar_version_guia, get_guia_default,
                          get_ruta_guia)
from ..ui_general import VistaGeneral
from .ui_ejercicios import SelectorEjercicios


class SelectorGuia(VistaGeneral):
    """
    Clase de una UI personalizada para cambiar de guías.
    """

    def __init__(self, version_actual: Optional[str]=None) -> None:
        """
        Inicializa una instancia de 'SelectorGuia'.
        """

        super().__init__()

        self.version_actual = version_actual


    @select(placeholder="Seleccione una versión de la guía",
            custom_id="selector_de_guia",
            options=[SelectOption(label=ver) for ver in lista_carpetas(get_ruta_guia())],
            max_values=1)
    async def seleccionar_guia(self, interaccion: Interaction, seleccion: Select) -> None:
        """
        Muestra y selecciona una versión específica de la guía.
        """

        version_vieja = self.version_actual
        nueva_version = seleccion.values[0] # Debería tener sólo un elemento
        self.version_actual = nueva_version

        actualizar_version_guia(nueva_version, interaccion.message.guild.id)

        formato_log = {"guild": interaccion.guild.name,
                       "old_ver": version_vieja,
                       "new_ver": nueva_version}

        self.log.info("En '%(guild)s', la versión de la guía fue cambiada " % formato_log +
                      "de %(old_ver)s a %(new_ver)s exitosamente" % formato_log)
        await interaccion.response.edit_message(content="**[AVISO]** La versión de la guía " +
                            f"fue cambiada{f' de `{version_vieja}`' if version_vieja else ''} a " +
                            f"`{nueva_version}` exitosamente.",
                                                view=None)


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
        guia: DiccionarioGuia=cargar_guia(get_guia_default())
    ) -> None:
        """
        Inicializa una instacia de 'MenuSelectorUnidad'.
        """

        self.guia = guia

        opciones = [SelectOption(label=f"Unidad {unidad}",
                                 description=self.guia[unidad]["titulo"],
                                 value=unidad)

                                 for unidad in lista_unidades(self.guia)]

        super().__init__(custom_id=custom_id,
                         placeholder=placeholder,
                         min_values=min_values,
                         max_values=max_values,
                         options=opciones,
                         disabled=disabled,
                         row=row)


    async def callback(self, interaccion: Interaction) -> None:
        """
        Procesa la unidad elegida por el usuario del menú selector.
        """

        unidad_elegida = self.values[0]

        vista = SelectorEjercicios(guia=self.guia, unidad=unidad_elegida)
        await interaccion.response.edit_message(content="Elija el ejercicio",
                                                view=vista)


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
