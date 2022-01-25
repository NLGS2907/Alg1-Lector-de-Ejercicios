"""
Módulo para funciones auxiliares del juego 'Piedra, Papel o Tijeras'.
"""

from discord import Message
from typing import Optional
from random import choice
from time import sleep

from ..archivos.archivos import DiccionarioStats, cargar_json, guardar_json
from ..constantes.constantes import PROPERTIES_PATH

def decidir_partida_ppt(eleccion: str, victoria: str, derrota: str, empate: str) -> Optional[int]:
    """
    Decide el resultado de una partida de 'Piedra, Papel o Tijeras'.

    Si 'eleccion' es igual que 'victoria', entonces se devuelve un '0'

    Si 'eleccion' es igual que 'derrota', entonces se devuelve un '1'.

    Si 'eleccion' es igual que 'empate', entonces se devuelve un '2'.

    Si no es igual que ninguna, se devuelve 'None'.
    """

    condicion_victoria = None

    if eleccion == victoria:

        condicion_victoria = 0

    elif eleccion == derrota:

        condicion_victoria = 1

    elif eleccion == empate:

        condicion_victoria = 2

    return condicion_victoria

async def jugar_partida_ppt(eleccion: str, author_id: str, msg: Message, stats_juego: DiccionarioStats) -> None:
    """
    Juega una partida de 'Piedra, Papel o Tijeras'.
    """

    opciones = ("PIEDRA", "PAPEL", "TIJERAS")
    piedra, papel, tijeras = opciones

    eleccion = eleccion.upper()
    opcion_elegida = choice(opciones)

    contenido_mensaje = f"¡Yo elegí `{opcion_elegida}`!"

    if msg.components:
    
        mensaje_partida = await msg.edit(content=contenido_mensaje, view=None)

    else:

        mensaje_partida = await msg.channel.send(content=contenido_mensaje, reference=msg.to_reference())

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

        stats_jugador[cond_partida] += 1
        stats_juego[author_id] = stats_jugador
        
        propiedades = cargar_json(PROPERTIES_PATH)
        propiedades["stats_ppt"] = stats_juego
        guardar_json(propiedades, PROPERTIES_PATH)

        contenido = None

        match cond_partida:

            case 0:

                contenido = "**¡Me ganaste!** ¡No, exijo otra!"

            case 1:

                contenido = "**¡Te gané!** ¡Tomá!"

            case 2:

                contenido = "**¡Es empate!**\n\n¿...pará, empate? ¡Otra!"

        victorias, derrotas, empates = stats_jugador

        aviso_stats = f"**Con esto,** llevás `{victorias}` Victorias, `{derrotas}` Derrotas y `{empates}` Empates."

        await mensaje_partida.edit(content=f"Vos elegiste `{eleccion}` y yo `{opcion_elegida}`:\n\n{contenido}\n\n{aviso_stats}")