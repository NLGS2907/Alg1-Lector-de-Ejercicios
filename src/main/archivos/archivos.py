"""
Módulo que procesa archivos.
"""

from json import dump, load
from os import listdir
from os.path import isdir, isfile, join, splitext
from typing import Optional

from ..constantes.constantes import EXT, GUIA_PATH, PROPERTIES_PATH

DiccionarioPares = dict[str, str]

DiccionarioGuia = dict[str, str | dict[str, str]]

DiccionarioStats = dict[str, list[int]]


def cargar_json(nombre_archivo: str) -> DiccionarioPares:
    """
    Lee y carga un archivo JSON.
    """
    dic_pares_valores = {}

    with open(nombre_archivo, mode='r', encoding="utf-8") as archivo:

        dic_pares_valores = load(archivo)

    return dic_pares_valores

def guardar_json(dic_pares_valores: DiccionarioPares, nombre_archivo: str, sangria: int=4) -> None:
    """
    Recibe un diccionario y guarda la informacion del mismo en un archivo JSON.
    """
    with open(nombre_archivo, mode='w', encoding="utf-8") as archivo:

        dump(dic_pares_valores, archivo, indent=sangria)


def archivos_guia(version: str, carpeta: str) -> list[str]:
    """
    Dado un directorio, devuelve una lista de strings con todos los nombres
    de los archivos que contienen las unidades de la guía, si y sólo si éstas
    son de la extensión utilizada para contener los enunciados.
    """

    version_path = join(carpeta, version)
    return [u for u in listdir(version_path)
            if (isfile(join(version_path, u)) and splitext(join(version_path, u))[1] == EXT)]


def lista_carpetas(carpeta: str=GUIA_PATH) -> list[str]:
    """
    Devuelve una lista de todas las carpetas que se encuentran en un
    directorio dado.
    """
    return [dir for dir in listdir(carpeta) if isdir(join(carpeta, dir))]


def version_es_valida(version: str, carpeta: str=GUIA_PATH) -> bool:
    """
    Verifica que la versión especificada existe dentro del directorio de
    las guías de ejercicios.
    """

    return version in lista_carpetas(carpeta)


def cargar_guia(version: str, carpeta: str=GUIA_PATH) -> Optional[DiccionarioGuia]:
    """
    Carga la guía de ejercicios en un diccionario de diccionarios, donde cada
    sub-diccionario tiene los pares clave valor en donde la clave es el numero
    de ejercicio y el valor el enunciado del mismo, ya formateado.

    Lanza una excepción si la versión pasada no es válida.
    """

    if not version_es_valida(version, carpeta):

        return None

    unidades = archivos_guia(version, carpeta)

    guia = {"version" : version}

    for unidad in range(1, len(unidades) + 1):

        dic_unidad = {}
        lista_ej = []
        nombre_ej = ''

        with open(f"{carpeta}/{version}/guia_{unidad}.txt", encoding="utf-8") as archivo:

            for linea in archivo:

                if any((not linea, linea == '\n', linea[0] == '#')):

                    continue

                llave, *valor = linea.rstrip().split('=', 1)
                valor = ''.join(valor)

                if llave == "titulo":

                    dic_unidad[llave] = valor

                elif valor == '<': # Empezar a leer ejercicio

                    nombre_ej = llave
                    lista_ej = []

                elif llave in ('t', 'n', 'tn', ''): # Para formatear lineas

                    tab = '\t' if llave in ('t', "tn") else ''
                    new_line = '\n' if llave in ('n', "tn") else ''

                    lista_ej.append(f"{tab}{valor}{new_line}")

                elif llave == '>': # Termina de leer ejercicio

                    dic_unidad[nombre_ej] = '\n'.join(lista_ej)

                else:

                    lista_ej.append(llave)

        guia[str(unidad)] = dic_unidad

    return guia

def lista_unidades(guia: DiccionarioGuia) -> list[str]:
    """
    Dada una guía, devuelve una lista de sus unidades.
    """

    copia_guia = guia.copy()
    copia_guia.pop("version") # Se escluye la clave 'version'

    return list(copia_guia)

def lista_ejercicios(guia: DiccionarioGuia, unidad: DiccionarioPares) -> list[str]:
    """
    Dada una guía de ejercicios y la unidad, devuelve una
    lista con los números de ejercicios.
    """

    copia_unidad = guia[unidad].copy()
    # Se excluye la clave 'titulo'
    copia_unidad.pop("titulo")

    return list(copia_unidad)

def actualizar_guia(nueva_version: str, guild_id: str) -> None:
    """
    Cambia la versión de la guía para un servidor en particular.
    """

    propiedades = cargar_json(PROPERTIES_PATH)
    propiedades["versiones_guia"][guild_id] = nueva_version
    guardar_json(propiedades, PROPERTIES_PATH)


def cargar_lineas(nombre_archivo: str) -> list[str]:
    """
    Devuelve una lista de las lineas de un archivo que tiene solo
    un valor en cada una.
    """

    lineas = []

    with open(nombre_archivo, encoding="utf-8") as archivo:

        for linea in archivo:

            lineas.append(linea.rstrip())

    return lineas
