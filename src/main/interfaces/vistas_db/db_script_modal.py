"""
Módulo para un modal de la DB que ejecuta scripts.
"""

from abc import ABC, abstractmethod
from sqlite3 import OperationalError

from discord import Interaction
from discord.enums import TextStyle
from discord.ui import Modal, TextInput

from ...db import CursorDesc, ejecutar_linea, ejecutar_script


class CommandDB(ABC, Modal):
    """
    Clase abstracta para modales de comandos de DB.
    """

    # Para rellenar, en realidad este nunca va a ser usado
    comando: TextInput = TextInput(label="script",
                                   style=TextStyle.paragraph,
                                   custom_id="db_cmd_command",
                                   placeholder="Escribe el script aquí...",
                                   required=True,
                                   row=0)


    def __init__(self) -> None:
        """
        Inicializa una instancia de 'CommandDB'.
        """

        super().__init__(timeout=None,
                         title=self.titulo(),
                         custom_id=self.id_custom())


    async def on_error(self, interaccion: Interaction, error: Exception) -> None:
        """
        Un error ocurrió.
        """

        msg = f"**[ERROR]** {str(error)}"
        await interaccion.response.send_message(content=msg,
                                                ephemeral=True)


    @abstractmethod
    def ejecutar(self, comando: str) -> CursorDesc:
        """
        Ejecuta el comando.
        """

        raise NotImplementedError


    @abstractmethod
    def titulo(self) -> str:
        """
        El título del modal.
        """

        raise NotImplementedError


    @abstractmethod
    def id_custom(self) -> str:
        """
        El id del modal.
        """

        raise NotImplementedError


    async def on_submit(self, interaccion: Interaction) -> None:
        """
        Envía el comando a la DB.
        """

        msg = ""

        try:
            desc = self.ejecutar(self.comando.value)
            filas = desc['rowcount']

            s = ('' if filas == 1 else 's')
            ron = ('' if filas == 1 else 'ron')
            msg_filas = f" `{filas}` *fila{s} fue{ron} afectada{s}.*"
            msg = f"*Operación exitosa.*{msg_filas if filas >= 0 else ''}"

        except SyntaxError:
            msg = "**[ERROR]:** *Sintaxis inválida.*"

        except OperationalError as e:
            msg = f"**[ERROR]:** {str(e)}"


        await interaccion.response.send_message(content=(msg
                                                         if msg.strip()
                                                         else "*Hmmm, parece que algo ocurrió.*"),
                                                ephemeral=True)


class ScriptDB(CommandDB):
    """
    Modal para ejecutar scripts en la DB.
    """

    comando: TextInput = TextInput(label="script",
                                   style=TextStyle.long,
                                   custom_id="db_script_command",
                                   placeholder="Escribe el script aquí...",
                                   required=True,
                                   row=0)


    def titulo(self) -> str:
        """
        Título del script.
        """

        return "Ejecutar Script"


    def id_custom(self) -> str:
        """
        El id del script.
        """

        return "db_script"


    def ejecutar(self, comando: str) -> CursorDesc:
        """
        Ejecuta el script.
        """

        return ejecutar_script(comando)


class LineaDB(CommandDB):
    """
    Modal para ejecutar scripts en la DB.
    """

    comando: TextInput = TextInput(label="comando de línea",
                                   style=TextStyle.short,
                                   custom_id="db_line_command",
                                   placeholder="Escribe el comando aquí...",
                                   required=True,
                                   row=0)


    def titulo(self) -> str:
        """
        Título del comando de línea.
        """

        return "Ejecutar Línea"


    def id_custom(self) -> str:
        """
        El id del comando de línea.
        """

        return "db_line"


    def ejecutar(self, comando: str) -> CursorDesc:
        """
        Ejecuta el comando de línea.
        """

        return ejecutar_linea(comando)
