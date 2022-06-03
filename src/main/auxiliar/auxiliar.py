"""
Módulo para funciones auxiliares
"""

from typing import TYPE_CHECKING

from discord import Interaction, Message, Thread
from discord.app_commands import check as appcheck

from ..archivos import cargar_json
from ..constantes import (ALGORITMOS_ESSAYA_ID, DEFAULT_PREFIX,
                          PROPERTIES_PATH, ROL_DIEGO_ID, ROL_DOCENTE_ID)

if TYPE_CHECKING:

    from ..lector import Lector


def es_rol_valido():
    """
    Verifica si está en el servidor del curso, y si es así,
    si se tienen los roles correspondientes.
    """

    def predicado(interaction: Interaction) -> bool:
        """
        Crea el check correspondiente.
        """

        return not all((interaction.guild.id == ALGORITMOS_ESSAYA_ID,
                        all([role.id not in (ROL_DIEGO_ID, ROL_DOCENTE_ID)
                             for role in interaction.user.roles])))

    return appcheck(predicado)


def es_hilo():
    """
    Verifica si la interacción ocurrió en un hilo.
    """

    def predicado(interaction: Interaction) -> bool:
        """
        Crea el check correspondiente.
        """

        return isinstance(interaction.channel, Thread)

    return appcheck(predicado)


def get_prefijo_por_id(guild_id: int) -> str:
    """
    Devuelve el prefijo de invocación de comandos dependiendo
    del guild donde se esté.
    """

    return cargar_json(PROPERTIES_PATH)["prefijos"].get(str(guild_id), DEFAULT_PREFIX)


def get_prefijo(_bot: "Lector", mensaje: Message) -> str:
    """
    Se fija en el diccionario de prefijos y devuelve el que
    corresponda al servidor de donde se convoca el comando.
    """

    return get_prefijo_por_id(mensaje.guild.id)
