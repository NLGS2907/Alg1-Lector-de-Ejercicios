"""
Módulo que procesa archivos.
"""

from json import dump, load
from os import PathLike
from pathlib import Path
from typing import Optional, TypeAlias, Union

from ..db import existe_dato_en_tabla, sacar_datos_de_tabla
from ..db.atajos import get_guia_default, get_guia_ext, get_ruta_guia
from ..logger import LectorLogger

DiccionarioPares: TypeAlias = dict[str, str]
DiccionarioEjercicio: TypeAlias = dict[str, Union[list[str], dict[str, list[str]]]]
DiccionarioUnidad: TypeAlias = dict[str, Union[str, DiccionarioEjercicio]]
DiccionarioGuia: TypeAlias = dict[str, Union[str, DiccionarioUnidad]]
DiccionarioStats: TypeAlias = dict[str, list[int]]


def cargar_json(ruta_archivo: PathLike) -> DiccionarioPares:
    """
    Lee y carga un archivo JSON.
    """

    dic_pares_valores = {}

    with open(ruta_archivo, mode='r', encoding="utf-8") as archivo:
        dic_pares_valores = load(archivo)

    return dic_pares_valores

def guardar_json(dic_pares_valores: DiccionarioPares,
                 ruta_archivo: PathLike,
                 *,
                 sangria: int=4) -> None:
    """
    Recibe un diccionario y guarda la informacion del mismo en un archivo JSON.
    """

    with open(ruta_archivo, mode='w', encoding="utf-8") as archivo:
        dump(dic_pares_valores, archivo, indent=sangria)


def lista_carpetas(carpeta: PathLike) -> list[PathLike]:
    """
    Devuelve una lista de todas las carpetas que se encuentran en un
    directorio dado.
    """

    path = Path(carpeta)
    return [p.name for p in path.iterdir() if p.is_dir()]


def lista_archivos(ruta: PathLike,
                   ext: Optional[str]=None,
                   ignorar_nombres: tuple[str, ...]=()) -> list[PathLike]:
    """
    Busca en la ruta especificada si hay archivos, y devuelve una lista
    con los nombres de los que encuentre.

    Si `ext` no es `None`, entonces probará buscando archivos con esa extensión.
    `ext` NO debe tener un punto (`.`) adelante, es decir que `"py"` será automáticamente
    tratado como `.py`.
    """

    path = Path(ruta)
    return [file.name
            for file in path.iterdir()
            if (file.is_file() and
                ((file.suffix == f".{ext}") if ext else True) and
                all(file.stem != nombre for nombre in ignorar_nombres))
            ]


def version_es_valida(version: str, carpeta_guias: PathLike="") -> bool:
    """
    Verifica que la versión especificada existe dentro del directorio de
    las guías de ejercicios.
    """

    if not carpeta_guias:
        carpeta_guias = get_ruta_guia()

    return version in lista_carpetas(carpeta_guias)


def archivos_guia(version: str, carpeta: PathLike) -> Optional[set[PathLike]]:
    """
    Dado un directorio, devuelve una lista de strings con todos los nombres
    de los archivos que contienen las unidades de la guía, si y sólo si éstas
    son de la extensión utilizada para contener los enunciados.
    """

    if not version_es_valida(version):
        return None

    ext = get_guia_ext()
    version_path = Path(carpeta) / version
    return set(u.name for u in version_path.iterdir()
               if (u.is_file() and
                   u.suffix == ext))

def cargar_guia(version: str, carpeta: PathLike="") -> Optional[DiccionarioGuia]:
    """
    Carga la guía de ejercicios en un diccionario de diccionarios, donde cada
    sub-diccionario tiene los pares clave valor en donde la clave es el numero
    de ejercicio y el valor el enunciado del mismo, ya formateado.

    Devuelve `None` si la versión pasada no es válida.
    """

    if not carpeta:
        carpeta = get_ruta_guia()

    if not version_es_valida(version, carpeta):
        return None

    unidades = archivos_guia(version, carpeta)
    guia = {"version" : version}
    ext = get_guia_ext()

    for unidad in range(1, len(unidades) + 1):
        guia[str(unidad)] = cargar_json(f"{carpeta}/{version}/guia_{unidad}{ext}")

    return guia

def lista_unidades(guia: DiccionarioGuia) -> list[str]:
    """
    Dada una guía, devuelve una lista de sus unidades.
    """

    copia_guia = guia.copy()
    copia_guia.pop("version") # Se escluye la clave especial 'version'

    return list(copia_guia)

def lista_ejercicios(guia: DiccionarioGuia, unidad: str) -> list[str]:
    """
    Dada una guía de ejercicios y la unidad, devuelve una
    lista con los números de ejercicios.
    """

    copia_unidad = guia[unidad].copy()
    copia_unidad.pop("titulo") # Se excluye la clave especial 'titulo'

    return list(copia_unidad)


def buscar_rutas(patron: str="*",
                 nombre_ruta: Optional[PathLike]=None,
                 recursivo: bool=True,
                 incluye_archivos: bool=True,
                 incluye_carpetas: bool=True,
                 ignorar_patrones: tuple[str, ...]=()) -> list[PathLike]:
    """
    Busca recursivamente en todas las subrutas por los archivos
    que coincidan con el patrón dado.
    Si `ruta` no está definida se usa el directorio actual.
    """

    ruta = Path(nombre_ruta if nombre_ruta is not None else ".")

    return list(fpath.as_posix() for fpath in (ruta.rglob(patron)
                                               if recursivo
                                               else ruta.glob(patron))
                if ((fpath.is_file() if incluye_archivos else False
                    or fpath.is_dir() if incluye_carpetas else False)
                    and all(not fpath.match(patr) for patr in ignorar_patrones)))


def buscar_archivos(patron: str="*",
                    nombre_ruta: Optional[PathLike]=None,
                    recursivo: bool=True,
                    ignorar_patrones: tuple[str, ...]=()) -> list[PathLike]:
    """
    Busca recursivamente en todas las subrutas por las rutas
    que coincidan con el patrón dado.
    Si `ruta` no está definida se usa el directorio actual.
    """

    return buscar_rutas(patron=patron,
                        nombre_ruta=nombre_ruta,
                        recursivo=recursivo,
                        incluye_archivos=True,
                        incluye_carpetas=False,
                        ignorar_patrones=ignorar_patrones)


def buscar_carpetas(patron: str="*",
                    nombre_ruta: Optional[PathLike]=None,
                    recursivo: bool=True,
                    ignorar_patrones: tuple[str, ...]=()) -> list[PathLike]:
    """
    Busca recursivamente en todas las subrutas por las carpetas
    que coincidan con el patrón dado.
    Si `ruta` no está definida se usa el directorio actual.
    """

    return buscar_rutas(patron=patron,
                        nombre_ruta=nombre_ruta,
                        recursivo=recursivo,
                        incluye_archivos=False,
                        incluye_carpetas=True,
                        ignorar_patrones=ignorar_patrones)


def get_version_guia_por_sv(guild_id: int) -> str:
    "Consigue la versión de guía de un servidor en específico."

    if existe_dato_en_tabla(tabla="guias",
                            guild_id=guild_id):
        return sacar_datos_de_tabla(tabla="guias",
                                    sacar_uno=True,
                                    guild_id=guild_id)[2]

    return get_guia_default()


def get_guia_por_sv(guild_id: int, version: Optional[str]=None) -> "DiccionarioGuia":
    "Carga una guía basada en la versión de su servidor."

    version = version or get_version_guia_por_sv(guild_id)
    version_a_usar = cargar_guia(version)
    log = LectorLogger()

    if version_a_usar is None:
        formato_log = {"version": version,
                        "default_ver": get_guia_default(),
                        "guild_id": guild_id}

        log.warning("La versión '%(version)s' no fue encontrada, " % formato_log +
                            "configurando la versión predeterminada " +
                            "'%(default_ver)s' para id %(guild_id)s..." % formato_log)
        version_a_usar = cargar_guia(get_guia_default())
        log.warning("listo.")

    return version_a_usar
