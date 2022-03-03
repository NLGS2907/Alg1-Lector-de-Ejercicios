"""
Registrador de eventos.
"""

from logging import (INFO, FileHandler, Formatter, Logger, StreamHandler,
                     getLogger)

from ..constantes import LOG_PATH


def nuevo_logger(nombre: str) -> Logger:
    """
    Genera un nuevo registrador.
    """

    formato_mensaje = "[ %(asctime)s ] - %(levelname)s - %(message)s"
    formato_fecha = "%d-%m-%Y %I:%M:%S %p" # Necesariamente distinto de DATE_FORMAT

    formateador = Formatter(fmt=formato_mensaje, datefmt=formato_fecha)

    archivo_handler = FileHandler(filename=LOG_PATH, encoding="utf-8")
    archivo_handler.setFormatter(formateador)

    consola_handler = StreamHandler()
    consola_handler.setFormatter(formateador)

    log_a_devolver = getLogger(name=nombre)
    log_a_devolver.setLevel(INFO)
    log_a_devolver.addHandler(archivo_handler)
    log_a_devolver.addHandler(consola_handler)

    return log_a_devolver


log = nuevo_logger("lector")
