"""
Módulo dedicado a contener al comportamiento del bot.
"""

import os
from typing import Optional
from random import choice
from datetime import datetime

from discord.ext import commands

import archivos

INFO_MESSAGE = """>>>\t**Lector de Ejercicios**



`!info` muestra esta lista.
`!ej <unidad> <ejercicio> | dm` para mostrar el ejercicio de la unidad correspondiente de la guía.

`!random <unidad_posible>, <opcion> | dm` para mostrar un ejercicio al azar. 'unidad_posible' es de
dónde empezar a buscar, y 'opcion' es el parámetro de búsqueda, y toma los valores '=', '<', '<=',
'>' o '>='.
Por ejemplo, *!random 12 <=* devuelve un ejercicio aleatorio de alguna guía anterior o igual a la guía 12.

*desarrolado por Franco 'NLGS' Lighterman.*
Repositorio de GitHub: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios
"""

CMD_PREFIX = os.environ["CMD_PREFIX"]
"""
El prefijo usado para identificar mensajes de comando
"""

GUIA = archivos.cargar_guia()
"""
Todos los enunciados de todas las unidades de la guía, ya
mapeados en un diccionario.
"""

EASTER_EGGS = archivos.cargar_easter_eggs()
"""
Pequeños guiños escondidos (más o menos).
"""

def existe_unidad(unidad: str, guia: dict=GUIA) -> bool:
    """
    Verifica si la unidad pasada existe dentro de la guía donde se guardan
    los ejercicios.

    Se sobreentiende que todas las claves de la guía son caracteres numéricos,
    y así debería mantenerse porque no se recomienda mutarlo.
    """

    return unidad in [parte for parte in guia.keys()]

def existe_ejercicio(ejercicio: str, unidad: str, guia: dict=GUIA) -> bool:
    """
    Verifica si un determinado ejercicio existe en una determinada unidad.
    """

    if not existe_unidad(unidad, guia):

        return False

    return ejercicio in [ej for ej in guia[unidad].keys()]



bot = commands.Bot(command_prefix=CMD_PREFIX)
"""
El objeto de tipo 'Bot' que maneja todo el comportamiento.
"""

@bot.event
async def on_ready() -> None:
    """
    El bot se conectó y está listo para usarse.
    """

    print(f"[ {str(datetime.now())} ] ¡{bot.user} conectado y listo para utilizarse!")

@bot.command(name="ej", help="Muestra ejercicios de la guía.")
async def leer_ejercicio(ctx, unidad: str, ejercicio: str, *opciones) -> None:

    if not existe_ejercicio(ejercicio, unidad):

        return

    enunciado = GUIA[unidad][ejercicio]
    mensaje = f"**{ctx.author.mention}** ha consultado:\n\n>>> **Unidad** {unidad} - \"{GUIA[unidad]['titulo']}\"  |  **Ejercicio** {ejercicio}:\n\n**{unidad}.{ejercicio}.** {enunciado}"

    if opciones and opciones[0] == "dm":

        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(mensaje)

    else:

        await ctx.channel.send(mensaje)

@bot.command(name="info", help="Muestra una lista de todos los comandos.")
async def mostrar_info(ctx, *opciones):
    """
    Muestra una lista con los comandos y lo que hace cada uno.
    """

    if opciones and opciones[0] == "dm":

        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(INFO_MESSAGE)

    else:

        await ctx.channel.send(INFO_MESSAGE)

@bot.command(name="random", help="Muestra un ejercicio aleatorio de la guía.")
async def ejercicio_al_azar(ctx, unidad_posible: Optional[str]=None, opcion: str='=', *opciones) -> None:
    """
    Muestra un ejercicio al azar de la guía.

    Si 'unidad_posible' es pasada y es válida, busca con esa unidad como pivote,
    siguiendo las instrucciones de 'opcion':

    '=' busca ejercicios solamente dentro de 'unidad_posible'.

    '<' busca ejercicios en unidades anteriores a la especificada.

    '<=' busca ejercicios en unidades anteriores y también en la especificada.

    '>' busca ejercicios en unidades posteriores a la especificada.

    '>=' busca ejercicios en unidades posteriores y también en la especificada.

    Todo funciona siempre en cuando las claves de la guia sean caracteres numéricos.
    """

    unidad_pivote = (unidad_posible if (unidad_posible and existe_unidad(unidad_posible, GUIA)) else choice(list(GUIA.keys())))
    expresion_busqueda = None
    unidad_elegida = ''
    ejercicio_elegido = ''

    if opcion == '=':

        unidad_elegida = unidad_pivote
        ejercicio_elegido = choice([ej for ej in GUIA[unidad_pivote].keys()])

    elif opcion == '<':

        expresion_busqueda = (lambda u: u < int(unidad_pivote))

    elif opcion == "<=":

        expresion_busqueda = (lambda u: u <= int(unidad_pivote))

    elif opcion == '>':

        expresion_busqueda = (lambda u: u > int(unidad_pivote))

    elif opcion == ">=":

        expresion_busqueda = (lambda u: u >= int(unidad_pivote))

    else: return

    if expresion_busqueda:

        unidad_elegida = choice([unidad for unidad in GUIA.keys() if expresion_busqueda(int(unidad))])
    
    ejercicio_elegido = choice([ej for ej in GUIA[unidad_elegida].keys()])

    await leer_ejercicio(ctx, unidad_elegida, ejercicio_elegido, ("dm" if (opciones and opciones[0] == "dm") else ''))

@bot.command(name="meme", help="Por si querés saber un poquito más.")
async def mostrar_easter_egg(ctx, *opciones):
    """
    Muestra una línea al azar del archivo de easter eggs.
    """

    if opciones and opciones[0] == "dm":

        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(choice(EASTER_EGGS))

    else:

        await ctx.channel.send(choice(EASTER_EGGS))

@bot.command(name="play", help="(¡Aún no implementado!)")
async def jugar(ctx):
    """
    Crea una instancia de juego.
    """

    await ctx.channel.send(f"`{ctx.prefix}{ctx.command}` *aún no ha sido implementado. ¡Pero vendrá muy pronto!*", delete_after=10)