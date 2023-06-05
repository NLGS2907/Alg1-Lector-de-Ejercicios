"""
Módulo dedicado a contener la clase personalizada 'CustomBot'.
"""

from platform import system
from typing import TYPE_CHECKING, Callable, Optional, TypeAlias

from discord import Game, Intents, Message
from discord.ext.commands import Bot
from discord.utils import utcnow

from ..ahorcado import Ahorcado
from ..archivos import buscar_archivos
from ..auxiliar import get_prefijo
from ..db.atajos import actualizar_guild, get_lector_id, get_ruta_cogs
from ..logger import LectorLogger

if TYPE_CHECKING:
    from datetime import datetime, timedelta

# Para que no tire error en Windows al cerrar el Bot.
try:
    from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except ImportError:
    LectorLogger().warning("No se pudo importar 'WindowsSelectorEventLoopPolicy', " +
                           "probablemente porque esto no es Windows.")

PrefixCallable: TypeAlias = Callable[["Lector", Message], str]
DiccionarioPartidas: TypeAlias = dict[str, Ahorcado]


# pylint: disable=abstract-method
class Lector(Bot):
    """
    Clase pasa sobrecargar y agregar cosas a la clase 'Bot'.
    """


    @staticmethod
    def intents_lector() -> Intents:
        """
        Crea un objeto `Intents` personalizado para este lector.
        """

        intents = Intents.default()
        intents.message_content = True # pylint: disable=assigning-non-slot

        return intents


    def __init__(self,
                 cmd_prefix: PrefixCallable=get_prefijo,
                 actividad=Game(name="leer ejercicios"),
                 **opciones) -> None:
        """
        Inicializa una instancia de tipo 'Lector'.
        """

        super().__init__(cmd_prefix,
                         activity=actividad,
                         intents=Lector.intents_lector(),
                         application_id=get_lector_id(),
                         options=opciones)

        self.inicializado_en: "datetime" = utcnow()
        "El momento exacto en que el bot fue inicializado."

        self.log: LectorLogger = LectorLogger()
        "Devuelve el logger del bot."

        self.partidas: DiccionarioPartidas = {}
        "Diccionario donde almacenar las partidas de ahorcado."


    async def setup_hook(self) -> None:
        """
        Reliza acciones iniciales que el bot necesita.
        """

        await self.cargar_cogs()


    async def cargar_cogs(self) -> None:
        """
        Busca y carga recursivamente todos los cogs
        del bot.
        """

        ext = "py"

        for ruta_cog in buscar_archivos(patron=f"*.{ext}",
                                        nombre_ruta=get_ruta_cogs(),
                                        ignorar_patrones=("__init__.*", "*_abc.*", "general.")):

            self.log.info(f"[COG] Cargando cog {ruta_cog!r}")
            await self.load_extension(ruta_cog.removesuffix(f".{ext}").replace("/", "."))

        self.log.info("Sincronizando arbol de comandos...")
        await self.tree.sync()


    def actualizar_db(self) -> None:
        """
        Hace todos los procedimientos necesarios para actualizar
        la base de datos de ser necesario.
        """

        self.log.info("[DB] Actualizando guilds...")
        for guild in self.guilds:
            actualizar_guild(guild.id, guild.name)


    @property
    def uptime(self) -> "timedelta":
        """
        Muestra cuánto tiempo el bot lleva activo.
        """

        return utcnow() - self.inicializado_en


    @staticmethod
    def es_ultimo_mensaje(msg: Message) -> bool:
        """
        Verifica que el mensaje a procesar no sea el
        ultimo del canal.
        """

        return msg == msg.channel.last_message


    def es_mensaje_de_bot(self, msg: Message) -> bool:
        """
        Verifica si un mensaje pasado es un mensaje escrito
        por el bot.
        """

        return not self.es_ultimo_mensaje(msg) and msg.author == self.user


    def es_mensaje_comando(self, msg: Message) -> bool:
        """
        Verifica si un mensaje escrito por un usuario o
        bot es un comando.
        """

        return ((not self.es_ultimo_mensaje(msg) and msg.content.startswith(get_prefijo(self, msg)))
                or self.es_mensaje_de_bot(msg))


    def encontrar_partida(self, id_a_encontrar: str) -> Optional[Ahorcado]:
        """
        Si la encuentra dentro del diccionario de partidas, devuelve la partida
        que corresponde al ID pasado.
        """

        partida_a_devolver = None

        for id_partida, partida in self.partidas.items():

            if str(id_a_encontrar) == id_partida:

                partida_a_devolver = partida
                break

        return partida_a_devolver
