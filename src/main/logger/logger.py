"""
Registrador de eventos.
"""

from logging import INFO, FileHandler, Formatter, StreamHandler, getLogger
from typing import TYPE_CHECKING

from ..db.atajos import get_ruta_log

if TYPE_CHECKING:

    from logging import Logger


class LectorLogger:
    """
    Clase que registra eventos del bot.
    Hecho con patrón singleton.
    """

    def __init__(self,
                 *,
                 nombre_log: str="lector",
                 nivel_log: int=INFO,
                 fmt: str="%(asctime)s - %(levelname)s - %(message)s",
                 fmt_fecha: str="%d-%m-%Y %I:%M:%S %p") -> None:
        """
        Crea una instancia de 'LectorLogger'.
        """

        super().__init__()

        self._formato: str = fmt
        self._fmt_fecha: str = fmt_fecha

        self._formateador = Formatter(fmt=self.formato, datefmt=self.fmt_fecha)

        self.handler_archivo = FileHandler(filename=get_ruta_log(), encoding="utf-8")
        self.handler_consola = StreamHandler()
        self.actualizar_formateador()

        self.logger: "Logger" = getLogger(nombre_log)
        self.logger.setLevel(nivel_log)
        self.logger.addHandler(self.handler_archivo)
        self.logger.addHandler(self.handler_consola)


    def actualizar_formateador(self) -> None:
        """
        Actualiza el formateador para cada handler que el logger tiene.
        """

        self.handler_archivo.setFormatter(self.formateador)
        self.handler_consola.setFormatter(self.formateador)


    @property
    def formateador(self) -> Formatter:
        """
        Devuelve el formateador en uso.
        """

        return self._formateador

    @formateador.setter
    def formateador(self, nuevo_formateador: Formatter) -> None:

        self._formateador = nuevo_formateador
        self.actualizar_formateador()


    @property
    def formato(self) -> str:
        """
        Devuelve el formato de los mensajes del log.
        """

        return self._formato


    @formato.setter
    def formato(self, nuevo_formato) -> None:

        self._formato = nuevo_formato
        self.formateador = Formatter(fmt=self.formato, datefmt=self.fmt_fecha)


    @property
    def fmt_fecha(self) -> str:
        """
        Devuelve el formato de fecha de los mensajes del log.
        """

        return self._fmt_fecha


    @fmt_fecha.setter
    def fmt_fecha(self, nuevo_fmt_fecha: str) -> None:

        self._fmt_fecha = nuevo_fmt_fecha
        self.formateador = Formatter(fmt=self.formato, datefmt=self.fmt_fecha)


    def debug(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel DEBUG.
        """

        self.logger.debug(mensaje, *args, **kwargs)


    def info(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel INFO.
        """

        self.logger.info(mensaje, *args, **kwargs)


    def warning(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel WARNING.
        """

        self.logger.warning(mensaje, *args, **kwargs)


    def error(self, mensaje: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel ERROR.
        """

        self.logger.error(mensaje, *args, **kwargs)


    def critical(self, message: str, *args, **kwargs) -> None:
        """
        Registra un evento de nivel CRITICAL.
        """

        self.logger.critical(message, *args, **kwargs)


    def exception(self, mensaje, *args, exc_info=True, **kwargs) -> None:
        """
        Registra una excepción.
        """

        self.logger.exception(mensaje, *args, exc_info, **kwargs)
