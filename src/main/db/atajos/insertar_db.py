"""
Módulo para atajos de INSERT.
"""

from ..database import (actualizar_dato_de_tabla, existe_dato_en_tabla,
                        insertar_datos_en_tabla)
from .sacar_db import get_prefijo_default, get_guia_default


def actualizar_guild(guild_id: int, nombre_guild: str) -> bool:
    """
    Registra el guild en la DB.

    Devuelve 'True' si el guild ya está presente, sino devuelve 'False'.
    """

    if existe_dato_en_tabla(tabla="guilds", id=guild_id):
        actualizar_dato_de_tabla(tabla="guilds",
                                 nombre_col="nombre",
                                 valor=nombre_guild,
                                 # condiciones,
                                 id=guild_id)
        return True

    insertar_datos_en_tabla(tabla="guilds",
                            llave_primaria_por_defecto=False,
                            valores=(guild_id, nombre_guild))
    actualizar_prefijo(get_prefijo_default(), guild_id)
    actualizar_version_guia(get_guia_default(), guild_id)
    return False


def actualizar_prefijo(nuevo_prefijo: str, guild_id: int) -> bool:
    """
    Actualiza el prefijo de un guild específico.

    Devuelve 'True' si el prefijo ya está presente, sino devuelve 'False'.
    """

    if existe_dato_en_tabla(tabla="prefijos", guild_id=guild_id):
        actualizar_dato_de_tabla(tabla="prefijos",
                                 nombre_col="prefijo",
                                 valor=nuevo_prefijo)
        return True

    insertar_datos_en_tabla(tabla="prefijos",
                            llave_primaria_por_defecto=True,
                            valores=(guild_id, nuevo_prefijo))
    return False


def actualizar_version_guia(nueva_guia: str, guild_id: int) -> bool:
    """
    Devuelve la versión de la guía de un guild específico.

    Devuelve 'True' si hay una versión presente, sino devuelve 'False'.
    """

    if existe_dato_en_tabla(tabla="guias", guild_id=guild_id):
        actualizar_dato_de_tabla(tabla="guias",
                                 nombre_col="guia",
                                 valor=nueva_guia)
        return True

    insertar_datos_en_tabla(tabla="guias",
                            llave_primaria_por_defecto=True,
                            valores=(guild_id, nueva_guia))
    return False
