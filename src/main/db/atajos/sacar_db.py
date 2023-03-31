"""
Módulo para atajos de sacar datos de una DB.
"""

from os import PathLike
from typing import TYPE_CHECKING, Tuple

from ..database import sacar_datos_de_tabla

if TYPE_CHECKING:
    from ..database import FetchResult


def get_propiedad(propiedad: str) -> "FetchResult":
    "Consigue alguna propiedad del lector."

    return sacar_datos_de_tabla("propiedades",
                                sacar_uno=True,
                                nombre=propiedad)[2]


def get_version() -> str:
    "Consigue la versión del lector."

    return get_propiedad("version")


def get_lector_id() -> int:
    "Consigue el ID del lector."

    return int(get_propiedad("lector_id"))


def get_prefijo_default() -> str:
    "Consigue el prefijo por defecto del lector."

    return get_propiedad("prefijo_default")


def get_sv_algo1_id() -> int:
    "Consigue el ID del servidor de 'Algoritmos y Programación 1 - Essaya'"

    return int(get_propiedad("sv_algo1_id"))


def get_rol_diego_id() -> int:
    "Consigue el ID del rol de Diego."

    return int(get_propiedad("rol_diego_id"))


def get_rol_docente_id() -> int:
    "Consigue el ID del rol de docente."

    return int(get_propiedad("rol_docente_id"))


def get_guia_default() -> str:
    "Consigue la versión predeterminada de la guía."

    return get_propiedad("guia_default")


def get_fmt_fecha() -> str:
    "Consigue el formato de fecha personalizado para el lector."

    return get_propiedad("fmt_fecha")


def get_guia_ext() -> str:
    "Consigue la extensión esperada para las unidades de las guías."

    return get_propiedad("guia_ext")


def get_ruta_de_db(nombre_ruta: str) -> PathLike:
    "Consigue una ruta de la DB."

    res = sacar_datos_de_tabla("rutas",
                               sacar_uno=True,
                               nombre_ruta=nombre_ruta)

    # El valor siempre será la tercera columna
    return res[2]


def get_rutas_de_db(nombre_ruta: str) -> Tuple[PathLike, ...]:
    "Consigue muchas rutas de la DB."

    res = sacar_datos_de_tabla("rutas",
                               sacar_uno=False,
                               nombre_ruta=nombre_ruta)

    # Los valores siempre serán la tercera columna
    return tuple(col[2] for col in res)


def get_prefijo_guild(guild_id: int) -> str:
    "Devuelve un prefijo por id del guild."

    res = sacar_datos_de_tabla("prefijos",
                               sacar_uno=True,
                               guild_id=guild_id)

    if not res:
        return get_prefijo_default()

    return res[2]


def get_ruta_guia() -> PathLike:
    "Consigue la ruta de las guías."

    return get_ruta_de_db("guia")


def get_ruta_cogs() -> PathLike:
    "Consigue la ruta de los cogs."

    return get_ruta_de_db("cogs")


def get_ruta_log() -> PathLike:
    "Consigue la ruta del log."

    return get_ruta_de_db("log")


def get_ruta_palabras() -> PathLike:
    "Consigue la ruta de las palabras de ahorcado."

    return get_ruta_de_db("palabras")
