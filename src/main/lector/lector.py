"""
Módulo dedicado a contener la clase personalizada 'CustomBot'.
"""

from platform import system
from typing import TYPE_CHECKING, Callable, Optional

from discord import Game, Intents, Interaction, Message
from discord.ext.commands import Bot
from discord.utils import utcnow

from ..ahorcado import Ahorcado
from ..archivos import (DiccionarioGuia, cargar_guia, cargar_json,
                        lista_archivos)
from ..auxiliar import get_prefijo
from ..constantes import (BOT_ID, BOT_VERSION, CLIENT_CONFIG, COGS_PATH,
                          DATE_FORMAT, DEFAULT_VERSION, PROPERTIES_PATH)
from ..imgur import Memegur
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
                 cmd_prefix: Callable=get_prefijo,
                 actividad=Game(name="leyendo ejercicios"),
                 **opciones) -> None:
        """
        Inicializa una instancia de tipo 'Lector'.
        """

        super().__init__(cmd_prefix,
                         activity=actividad,
                         intents=Lector.intents_lector(),
                         application_id=BOT_ID,
                         options=opciones)

        propiedades = cargar_json(PROPERTIES_PATH)

        self.inicializado_en: "datetime" = utcnow()
        """
        El momento exacto en que el bot fue inicializado.
        """

        self.version: str = BOT_VERSION
        """
        La versión actual del bot.
        """

        self.cliente_imgur: Memegur = Memegur(CLIENT_CONFIG)
        """
        El cliente de Imgur encargado de manejar las imágenes que pide el bot.
        """

        self.guias = self.definir_guias()
        """
        El diccionario de guías, posiblemente diferente para cada servidor.
        """

        self.partidas = {}
        """
        Diccionario donde almacenar las partidas de ahorcado.
        """

        self.rps_stats = propiedades["stats_ppt"]


    async def setup_hook(self) -> None:
        """
        Reliza acciones iniciales que el bot necesita.
        """

        ext = "py"

        for cog_name in lista_archivos(COGS_PATH, ext=ext):
            if cog_name == "__init__.py":
                continue

            await self.load_extension(f".{cog_name.removesuffix(f'.{ext}')}",
                                      package="src.main.cogs")

        await self.tree.sync()


    @property
    def log(self) -> LectorLogger:
        """
        Devuelve el logger del bot.
        """

        return LectorLogger()


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


    def definir_guias(self) -> dict[str, DiccionarioGuia]:
        """
        Define todas las versiones de la guía, diferenciable en cada servidor,
        con posibilidad de cambiarla en algún momento en el futuro.
        """

        dict_guias = {}
        propiedades_guias = cargar_json(PROPERTIES_PATH)["versiones_guia"]

        for guild_id, version in propiedades_guias.items():

            version_a_usar = cargar_guia(version)

            if version_a_usar is None:

                formato_log = {"version": version,
                               "default_ver": DEFAULT_VERSION,
                               "guild_id": guild_id}

                self.log.warning("La versión '%(version)s' no fue encontrada, " % formato_log +
                            "configurando la versión predeterminada " +
                            "'%(default_ver)s' para id %(guild_id)s..." % formato_log)
                version_a_usar = DEFAULT_VERSION
                self.log.warning("listo.")

            dict_guias[guild_id] = version_a_usar

        return dict_guias


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


    def actualizar_guia(self) -> None:
        """
        Actualia el atributo 'self.guias' para que sea acorde a la información
        guardada en los archivos.
        """

        self.guias = self.definir_guias()


    async def hanged_create(self,
                            interaction: Interaction,
                            palabras: Optional[str],
                            vidas: int) -> None:
        """
        Inicializa una sala de juego.
        """

        await interaction.response.send_message("¡Partida Creada!",
                                                ephemeral=True)
        mensaje_pivote = await interaction.channel.send("¡Partida de ahorcado en juego!")
        hilo = await mensaje_pivote.create_thread(name="AHORCADO - Partida " +
                                                    f"{self.inicializado_en.strftime(DATE_FORMAT)}",
                                                  auto_archive_duration=60,
                                                  reason="Alguien quiere jugar al ahorcado.")
        frase_a_usar = None

        spoilertag = "||"  # Por si el usuario la declaró con spoilertags
        frase = (' '.join(palabras.replace(spoilertag, '').split())
                 if palabras is not None
                 else None)

        if frase: # El usuario indicó una con la que jugar
            frase_a_usar = frase

        self.partidas[str(hilo.id)] = Ahorcado(frase=frase_a_usar,
                                               vidas_maximas=vidas,
                                               id_mensaje_padre=mensaje_pivote.id)
        partida = self.partidas[str(hilo.id)]
        mensaje = await hilo.send(partida)
        partida.definir_display(mensaje.id)


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


    async def hanged_guess(self, interaction: Interaction, char: str) -> None:
        """
        Intenta adivinar una letra u otro caracter, si no fue usado ya.
        """

        if not char:
            await interaction.response.send_message(content=f"**[ERROR]** `{char}` no es " +
                                                            "una letra válida.",
                                                    ephemeral=True)
            return

        partida = self.encontrar_partida(str(interaction.channel.id))

        # 'letra' debe ser, efectivamente, una cadena de un solo caracter
        if any((not partida, partida.intentos <= 0, not len(char) == 1)):
            await interaction.response.send_message(content=f"**[ERROR]** `{char}` debe ser " +
                                                            "una cadena de un sólo caracter.",
                                                    ephemeral=True)
            return

        fue_usado, esta_presente = partida.adivinar(char)
        char = char.upper()

        if fue_usado:
            await interaction.response.send_message(f"¡Mal ahí, {interaction.user.mention}! " +
                                                    f"¡El caracter `{char}` ya fue utilizado! " +
                                                    "Probá con otra cosa...")
            return

        if esta_presente:
            await interaction.response.send_message(f"¡{interaction.user.mention} ha acertado " +
                                                    f"el caracter `{char}`!")

        else:
            await interaction.response.send_message(f"¡Ole! ¡{interaction.user.mention} ha " +
                                                    f"dicho el caracter `{char}`, " +
                                                    "que no se encuentra en la palabra! " +
                                                    f"Quedan {partida.intentos} intento/s...")

        mensaje = await interaction.channel.fetch_message(partida.display_id)
        await mensaje.edit(content=str(partida))


    async def fin_del_juego(self, interaction: Interaction, es_victoria: bool) -> None:
        """
        Hace las acciones correspondientes una vez que termina el juego.
        """

        partida_terminada: Ahorcado = self.partidas.pop(str(interaction.channel.id))
        frase_magica = ''.join([c.valor for c in partida_terminada.frase])
        ultimo_caracter = partida_terminada.caracteres_usados.pop()
        es_una_vida = (partida_terminada.intentos == 1)

        if es_victoria:

            contenido = (f"Resultado de partida `{interaction.channel.name}`: " +
            f"**[VICTORIA]**\n\n¡{interaction.user.mention} se hizo con la victoria con la letra " +
            f"`{ultimo_caracter}`, y con `{partida_terminada.intentos}` " +
            f"vida{'' if es_una_vida else 's'} de sobra! En efecto, la frase era `{frase_magica}`.")

            await interaction.channel.parent.send(content=contenido)

        else:

            contenido = (f"Resultado de partida `{interaction.channel.name}`: **[DERROTA]**" +
            f"\n\n¡Vergüenza para {interaction.user.mention}! Ha fastidiado la partida " +
            f"diciendo el caracter `{ultimo_caracter}`. La frase era `{frase_magica}`.")

            await interaction.channel.parent.send(content=contenido)

        mensaje_original = await interaction.channel\
                           .parent.fetch_message(partida_terminada.id_mensaje_padre)
        if mensaje_original:
            await mensaje_original.delete()
        await interaction.channel.delete()
