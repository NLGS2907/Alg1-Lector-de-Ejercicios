"""
Módulo para funciones de autocompletado.
"""

from typing import TYPE_CHECKING

from discord import Interaction
from discord.app_commands import Choice

from ..db import nombres_tablas


async def autocompletado_nombres_tablas_db(_interaccion: Interaction,
                                           current: str) -> list[Choice[str]]:
    """
    Devuelve los nombres de todas las tablas disponibles en la DB.
    """

    return [
        Choice(name=tabla, value=tabla) for tabla in nombres_tablas()
        if current.lower() in tabla.lower()
    ][:25]