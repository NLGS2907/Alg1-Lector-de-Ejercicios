"""
Módulo para funciones auxiliares del juego 'Piedra, Papel o Tijeras'.
"""

from random import choice
from time import sleep
from typing import Optional

from discord import Message

from ..archivos import DiccionarioStats, cargar_json, guardar_json
from ..constantes import PROPERTIES_PATH
from .condicion_partida import Condicion


def decidir_partida_ppt(eleccion: str,
                        victoria: str,
                        derrota: str,
                        empate: str) -> Optional[Condicion]:
    """
    Decide el resultado de una partida de 'Piedra, Papel o Tijeras'.

    Si 'eleccion' es igual que 'victoria', entonces se devuelve un '0'

    Si 'eleccion' es igual que 'derrota', entonces se devuelve un '1'.

    Si 'eleccion' es igual que 'empate', entonces se devuelve un '2'.

    Si no es igual que ninguna, se devuelve 'None'.
    """

    condicion_victoria = None

    if eleccion == victoria:

        condicion_victoria = Condicion.VICTORIA

    elif eleccion == derrota:

        condicion_victoria = Condicion.DERROTA

    elif eleccion == empate:

        condicion_victoria = Condicion.EMPATE

    return condicion_victoria

async def jugar_partida_ppt(eleccion: str,
                            author_id: str,
                            msg: Message,
                            stats_juego: DiccionarioStats) -> None:
    """
    Juega una partida de 'Piedra, Papel o Tijeras'.
    """

    opciones = ("PIEDRA", "PAPEL", "TIJERAS")

    eleccion = eleccion.upper()
    opcion_elegida = choice(opciones)

    piedra, papel, tijeras = opciones

    contenido_mensaje = f"¡Yo elegí `{opcion_elegida}`!"

    if msg.components:

        mensaje_partida = await msg.edit(content=contenido_mensaje, view=None)

    else:

        mensaje_partida = await msg.channel.send(content=contenido_mensaje,
                                                 reference=msg.to_reference())

    sleep(2.0) # suspenso...

    stats_jugador = stats_juego.get(author_id, [0, 0, 0])

    match eleccion:

        case "PIEDRA":

            cond_partida = decidir_partida_ppt(opcion_elegida, tijeras, papel, piedra)

        case "PAPEL":

            cond_partida = decidir_partida_ppt(opcion_elegida, piedra, tijeras, papel)

        case "TIJERAS":

            cond_partida = decidir_partida_ppt(opcion_elegida, papel, piedra, tijeras)

        case _:

            cond_partida = None

    if cond_partida is not None:

        stats_jugador[cond_partida.value] += 1
        stats_juego[author_id] = stats_jugador

        propiedades = cargar_json(PROPERTIES_PATH)
        propiedades["stats_ppt"] = stats_juego
        guardar_json(propiedades, PROPERTIES_PATH)

        contenido = None

        match cond_partida:

            case Condicion.VICTORIA:

                contenido = "**¡Me ganaste!** ¡No, exijo otra!"

            case Condicion.DERROTA:

                contenido = "**¡Te gané!** ¡Tomá!"

            case Condicion.EMPATE:

                contenido = "**¡Es empate!**\n\n¿...pará, empate? ¡Otra!"

        victorias, derrotas, empates = stats_jugador

        aviso_stats = (f"**Con esto,** llevás `{victorias}` Victorias, `{derrotas}` Derrotas " +
                       f"y `{empates}` Empates.")

        await mensaje_partida.edit(content=f"Vos elegiste `{eleccion}` y yo `{opcion_elegida}`:" +
                                           f"\n\n{contenido}\n\n{aviso_stats}",
                                   delete_after=10.0,
                                   view=None)
