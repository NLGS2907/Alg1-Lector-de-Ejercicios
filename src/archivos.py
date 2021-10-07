from csv import reader
from os import listdir
from os.path import isfile, isdir, join, splitext
from typing import Union

EXT = ".txt"
"""
La extensión de archivo usada para almacenar el texto que son los ejercicios
de la guía.
"""

GUIA_PATH = "guia"
"""
Dirección (relativa) de la carpeta de guías.
"""

DiccionarioPares = dict[str, str]

DiccionarioGuia = dict[str, Union[str, dict[str, str]]]

class GuiaNoEncontrada(Exception):
    """
    Pequeña clase para definir un error de guía no encontrada.
    """

    pass

def archivos_guia(version: str, carpeta: str) -> list[str]:
    """
    Dado un directorio, devuelve una lista de strings con todos los nombres
    de los archivos que contienen las unidades de la guía, si y sólo si éstas
    son de la extensión utilizada para contener los enunciados.
    """

    version_path = join(carpeta, version)
    return [u for u in listdir(version_path) if (isfile(join(version_path, u)) and splitext(join(version_path, u))[1] == EXT)]

def lista_versiones(carpeta: str=GUIA_PATH):
    """
    Devuelve una lista de todas las versiones válidas que se encuentran
    en el directorio de guías.
    """
    return [ver for ver in listdir(carpeta) if isdir(join(carpeta, ver))]

def version_es_valida(version: str, carpeta: str=GUIA_PATH):
    """
    Verifica que la versión especificada existe dentro del directorio de
    las guías de ejercicios.
    """

    return version in lista_versiones(carpeta)

def cargar_guia(version: str, carpeta: str=GUIA_PATH) -> DiccionarioGuia:
    """
    Carga la guía de ejercicios en un diccionario de diccionarios, donde cada
    sub-diccionario tiene los pares clave valor en donde la clave es el numero
    de ejercicio y el valor el enunciado del mismo, ya formateado.

    Lanza una excepción si la versión pasada no es válida.
    """

    if not version_es_valida(version, carpeta):

        raise GuiaNoEncontrada(f"La versión especificada '{version}' no es válida. No se puede cargar un diccionario inexistente.")

    unidades = archivos_guia(version, carpeta)

    guia = {"version" : version}

    for unidad in range(1, len(unidades) + 1):

        dic_unidad = dict()
        lista_ej = list()
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
                    lista_ej = list()

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

def cargar_lineas(nombre_archivo: str) -> list[str]:
    """
    Devuelve una lista de las lineas de un archivo que tiene solo
    un valor en cada una.
    """

    lineas = list()

    with open(nombre_archivo, encoding="utf-8") as archivo:

        for linea in archivo:

            lineas.append(linea.rstrip())

    return lineas

def cargar_pares_valores(nombre_archivo: str) -> DiccionarioPares:
    """
    Lee el archivo de prefijos y devuelve un diccionario con
    cada server y su prefijo asignado mapeados en un diccionario.
    """

    dic_pares_valores = dict()

    with open(nombre_archivo, 'r') as archivo:

        prefijos = reader(archivo, delimiter='=')

        for clave, valor in prefijos:

            dic_pares_valores[clave] = valor

    return dic_pares_valores

def guardar_pares_valores(dic_pares_valores: DiccionarioPares, nombre_archivo: str) -> None:
    """
    Recibe un diccionario y guarda la información de este en un archivo CSV.
    """

    lista_a_imprimir = list()

    with open(nombre_archivo, 'w') as archivo:

        for clave, valor in dic_pares_valores.items():

            lista_a_imprimir.append(f"{clave}={valor}")

        archivo.write('\n'.join(lista_a_imprimir))