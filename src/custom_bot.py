from typing import Callable, Optional

from discord import Message
from discord.guild import Guild
from discord.ext import commands

from datetime import datetime

import ahorcado
import archivos

DEFAULT_PREFIX = '!'
"""
El prefijo por defecto que los servidores a los que se una el bot
tendrá inicialmente.
"""

DEFAULT_VERSION = "2c2019"
"""
La versión de la guía por defecto, si la especificada no se encontrase.
"""

PREFIXES_FILE = "src/prefixes.csv"

VERSIONS_FILE = "src/versions.csv"

def get_prefijo(bot, mensaje: Message) -> str:
    """
    Se fija en el diccionario de prefijos y devuelve el que
    corresponda al servidor de donde se convoca el comando.
    """

    return archivos.cargar_pares_valores(PREFIXES_FILE).get(str(mensaje.guild.id), DEFAULT_PREFIX)

def get_version(guild: Guild) -> str:
    """
    Consigue la versión de la guía que ha sido especificada, si no
    devuelve el valor predeterminado como constante.
    """

    return archivos.cargar_pares_valores(VERSIONS_FILE).get(str(guild.id), DEFAULT_VERSION)

def definir_guias() -> dict[str, archivos.DiccionarioGuia]:
    """
    Define todas las versiones de la guía, diferenciable en cada servidor,
    con posibilidad de cambiarla en algún momento en el futuro.
    """

    dict_guias = dict()

    for guild_id, version in archivos.cargar_pares_valores(VERSIONS_FILE).items():

        try:

            dict_guias[guild_id] = archivos.cargar_guia(version)

        except archivos.GuiaNoEncontrada:

            print(f"[AVISO] La versión '{version}' no fue encontrada, configurando la versión predeterminada '{DEFAULT_VERSION}' para id {guild_id}...", end=' ')

            dict_guias[guild_id] = DEFAULT_VERSION

            print("listo.")

    return dict_guias

class CustomBot(commands.Bot):
    """
    Clase pasa sobrecargar y agregar cosas a la clase 'commands.Bot'.
    """

    def __init__(self, cmd_prefix: Callable=get_prefijo, **opciones) -> None:
        """
        Crea una instancia de tipo 'CustomBot'.
        """

        super().__init__(cmd_prefix, options=opciones)

        self.guias = definir_guias()
        """
        El diccionario de guías, posiblemente diferente para cada servidor.
        """

        self.partidas = dict()

    async def hanged_create(self, ctx: commands.Context, vidas: int, *palabras) -> None:
        """
        Crea una sala de juego.
        """

        hilo = await ctx.message.create_thread(name=f"AHORCADO - Partida {datetime.now()}", auto_archive_duration=60)
        frase_a_usar = None

        spoilertag = "||"  # Por si el usuario la declaró con spoilertags
        frase = ' '.join(' '.join(palabras).replace(spoilertag, '').split()).upper()

        if frase:  # El usuario indicó una  con la que jugar

            frase_a_usar = frase

        self.partidas[str(hilo.id)] = ahorcado.Ahorcado(frase_a_usar, vidas_maximas=vidas)
        partida = self.partidas[str(hilo.id)]
        mensaje = await hilo.send(partida)
        partida.definir_display(mensaje.id)

    def encontrar_partida(self, id_a_encontrar: str) -> Optional[ahorcado.Ahorcado]:
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

    async def hanged_guess(self, ctx: commands.Context, char: str) -> None:
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

    async def fin_del_juego(self, ctx: commands.Context, es_victoria: bool) -> None:
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
