"""
Módulo para funciones auxiliares
"""

from typing import TYPE_CHECKING

from discord import Message

from ..db.atajos import get_prefijo_default, get_prefijo_guild

if TYPE_CHECKING:

    from ..lector import Lector


def get_prefijo(_bot: "Lector", mensaje: Message) -> str:
    """
    Se fija en el diccionario de prefijos y devuelve el que
    corresponda al servidor de donde se convoca el comando.
    """

    if mensaje.guild is None:
        return get_prefijo_default()

    return get_prefijo_guild(guild_id=mensaje.guild.id)
