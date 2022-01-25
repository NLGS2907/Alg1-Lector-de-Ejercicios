"""
Módulo dedicado a contener la clase personalizada 'CustomBot'.
"""

from typing import Callable, Optional
from discord import Message, Game
from discord.ext.commands import Bot, Context
from datetime import datetime

from ..auxiliar.auxiliar import get_prefijo
from ..imgur.cliente import MemeImgur
from ..logger.logger import log
from ..cogs.ejercicios import CogEjercicios
from ..cogs.hanged import CogHanged
from ..cogs.rps import CogRPS
from ..cogs.admin import CogAdmin
from ..cogs.eventos import CogEventos
from ..cogs.imgur import CogImgur
from ..cogs.misc import CogMisc
from ..ahorcado.ahorcado import Ahorcado
from ..archivos.archivos import cargar_guia, cargar_json, DiccionarioGuia

from ..constantes.constantes import BOT_VERSION, DATE_FORMAT, DEFAULT_VERSION, PROPERTIES_PATH

# Para que no tire error en Windows al cerrar el Bot.

from platform import system
from asyncio import set_event_loop_policy

try:

    from asyncio import WindowsSelectorEventLoopPolicy

    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())

except ImportError:

    log.warning("No se pudo importar 'WindowsSelectorEventLoopPolicy', probablemente porque esto no es Windows.")


class Lector(Bot):
    """
    Clase pasa sobrecargar y agregar cosas a la clase 'Bot'.
    """

    @staticmethod
    def definir_guias() -> dict[str, DiccionarioGuia]:
        """
        Define todas las versiones de la guía, diferenciable en cada servidor,
        con posibilidad de cambiarla en algún momento en el futuro.
        """

        dict_guias = dict()
        propiedades_guias = cargar_json(PROPERTIES_PATH)["versiones_guia"]

        for guild_id, version in propiedades_guias.items():

            version_a_usar = cargar_guia(version)

            if version_a_usar is None:

                log.warning(f"La versión '{version}' no fue encontrada, configurando la versión predeterminada '{DEFAULT_VERSION}' para id {guild_id}...")
                version_a_usar = DEFAULT_VERSION
                log.warning("listo.")

        dict_guias[guild_id] = version_a_usar
        return dict_guias


    def __init__(self, cmd_prefix: Callable=get_prefijo, actividad=Game(name="!info"), **opciones) -> None:
        """
        Inicializa una instancia de tipo 'CustomBot'.
        """

        super().__init__(cmd_prefix, activity=actividad, options=opciones)

        propiedades = cargar_json(PROPERTIES_PATH)

        self.version = BOT_VERSION
        """
        La versión actual del bot.
        """

        self.cliente = MemeImgur()
        """
        El cliente de Imgur encargado de manejar las imágenes que pide el bot.
        """

        self.guias = Lector.definir_guias()
        """
        El diccionario de guías, posiblemente diferente para cada servidor.
        """

        self.partidas = dict()
        """
        Diccionario donde almacenar las partidas de ahorcado.
        """

        self.rps_stats = propiedades["stats_ppt"]

        self.add_cog(CogEventos(self))
        self.add_cog(CogImgur(self))
        self.add_cog(CogMisc(self))
        self.add_cog(CogAdmin(self))
        self.add_cog(CogEjercicios(self))
        self.add_cog(CogHanged(self))
        self.add_cog(CogRPS(self))


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

        return (not self.es_ultimo_mensaje(msg) and msg.content.startswith(get_prefijo(self, msg))) or self.es_mensaje_de_bot(msg)


    def actualizar_guia(self) -> None:
        """
        Actualia el atributo 'self.guias' para que sea acorde a la información
        guardada en los archivos.
        """

        self.guias = Lector.definir_guias()


    async def hanged_create(self, ctx: Context, vidas: int, *palabras) -> None:
        """
        Inicializa una sala de juego.
        """

        hilo = await ctx.message.create_thread(name=f"AHORCADO - Partida {datetime.now().strftime(DATE_FORMAT)}", auto_archive_duration=60)
        frase_a_usar = None

        spoilertag = "||"  # Por si el usuario la declaró con spoilertags
        frase = ' '.join(' '.join(palabras).replace(spoilertag, '').split()).upper()

        if frase:  # El usuario indicó una  con la que jugar

            frase_a_usar = frase

        self.partidas[str(hilo.id)] = Ahorcado(frase_a_usar, vidas_maximas=vidas)
        partida = self.partidas[str(hilo.id)]
        mensaje = await hilo.send(partida)
        partida.definir_display(mensaje.id)


    def encontrar_partida(self, id_a_encontrar: str) -> Optional[Ahorcado]:
        """
        Si la encuentra dentro del diccionario de partidas, devuelve la partida
        que corresponde al ID pasado.
        """

        partida = None

        for id_partida in self.partidas:

            if str(id_a_encontrar) == id_partida:

                partida = self.partidas[id_partida]
                break

        return partida


    async def hanged_guess(self, ctx: Context, char: str) -> None:
        """
        Intenta adivinar una letra u otro caracter, si no fue usado ya.
        """

        if not char:

            return

        partida = self.encontrar_partida(str(ctx.channel.id))

        if any((not partida, partida.intentos <= 0, not len(char) == 1)):  # 'letra' debe ser, efectivamente, uan cadena de un solo caracter

            return

        char = char.upper()

        if char in partida.caracteres_usados:

            await ctx.channel.send(f"¡Mal ahí, {ctx.author.mention}! ¡El caracter `{char}` ya fue utilizado! Probá con otra cosa...")
            return

        if char in [l.valor for l in partida.frase]:

            for letrita in partida.frase:

                if letrita.valor == char:

                    letrita.oculta = False

            await ctx.channel.send(f"¡{ctx.author.mention} ha acertado el caracter `{char}`!")

        else:

            partida.intentos -= 1
            await ctx.channel.send(f"¡Ole! ¡{ctx.author.mention} ha dicho el caracter `{char}`, que no se encuentra en la palabra! Quedan {partida.intentos} intentos...")

        partida.caracteres_usados.append(char)

        mensaje = await ctx.channel.fetch_message(partida.display_id)
        await mensaje.edit(str(partida))


    async def fin_del_juego(self, ctx: Context, es_victoria: bool) -> None:
        """
        Hace las acciones correspondientes una vez que termina el juego.
        """

        partida_terminada = self.partidas.pop(str(ctx.channel.id))
        frase_magica = ''.join([c.valor for c in partida_terminada.frase])
        ultimo_caracter = partida_terminada.caracteres_usados.pop()
        es_una_vida = (partida_terminada.intentos == 1)

        if es_victoria:

            await ctx.channel.parent.send(f"Resultado de partida `{ctx.channel.name}`: **[VICTORIA]**\n\n¡{ctx.author.mention} se hizo con la victoria con la letra `{ultimo_caracter}`, y con `{partida_terminada.intentos}` vida{'' if es_una_vida else 's'} de sobra! En efecto, la frase era `{frase_magica}`.")

        else:

            await ctx.channel.parent.send(f"Resultado de partida `{ctx.channel.name}`: **[DERROTA]**\n\n¡Vergüenza para {ctx.author.mention}! Ha fastidiado la partida diciendo el caracter `{ultimo_caracter}`. La frase era `{frase_magica}`.")

        await ctx.channel.delete()
