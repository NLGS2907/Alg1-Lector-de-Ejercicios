"""
Registrador de eventos.
"""

import logging

from ..constantes.constantes import LOG_PATH


def nuevo_logger(nombre: str) -> logging.Logger:
    """
    Genera un nuevo registrador.
    """

    formato_mensaje = "[ %(asctime)s ] - %(levelname)s - %(message)s"
    formato_fecha = "%d-%m-%Y %I:%M:%S %p" # Necesariamente distinto de DATE_FORMAT

    formateador = logging.Formatter(fmt=formato_mensaje, datefmt=formato_fecha)

    archivo_handler = logging.FileHandler(filename=LOG_PATH, encoding="utf-8")
    archivo_handler.setFormatter(formateador)

    consola_handler = logging.StreamHandler()
    consola_handler.setFormatter(formateador)

    log_a_devolver = logging.getLogger(name=nombre)
    log_a_devolver.setLevel(logging.INFO)
    log_a_devolver.addHandler(archivo_handler)
    log_a_devolver.addHandler(consola_handler)

    return log_a_devolver


log = nuevo_logger("lector")
