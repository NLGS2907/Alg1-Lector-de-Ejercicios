"""
Módulo dedicado a contener al comportamiento del bot.
"""

from typing import Optional
from random import choice
from datetime import datetime

from discord import Thread
from discord.ext.commands import Context

import custom_bot, archivos

ALGORITMOS_ESSAYA_ID = 653341065767550976
"""
Para más facilidad, se tiene a mano una constante
con el ID del servidor de Algoritmos I - Essaya.
"""

ROL_DIEGO_ID = 653341579389435927

ROL_DOCENTE_ID = 653341523886342145

INFO_MESSAGE = """>>> **Lector de Ejercicios - Instrucciones**

Versión de la guía para este servidor: `{version}`

`{prefix}info` muestra esta lista.

`{prefix}ej|ejercicio|enunciado <unidad> <ejercicio> | dm` para mostrar el ejercicio de la unidad correspondiente de la guía.

`{prefix}random|aleatorio|r <unidad_posible>, <sentido> | dm` para mostrar un ejercicio al azar. 'unidad_posible' es de
dónde empezar a buscar, y 'sentido' es el parámetro de búsqueda, y toma los valores '=', '<', '<=',
'>' o '>='.
Por ejemplo, `{prefix}random 12 <=` devuelve un ejercicio aleatorio de alguna guía anterior o igual a la guía 12.

`{prefix}prefix|prefijo <nuevo_prefijo>` cambia el prefijo de los comandos a 'nuevo_prefijo'.

`{prefix}guia|version <nueva_version>` cambia la versión de la guía que utilizar, si es una versión válida.

`{prefix}meme <id>` para generar un meme aleatorio, o con `<id>` determinado si se desea uno en concreto, aunque
hay que conocer el URL del meme en específico (solo funciona si tiene el dominio `https://i.imgur.com`).

`{prefix}hanged|ahorcado <vidas> <*frase>` para reservar una sala de ahorcado. Esta es en forma de un hilo temporal.
Si se hace una partida personalizada con `<*frase>` determinada por el usuario, se recomienda encerrarlo en '\|\|'.
Así, \|\|palabra\|\| se ve como ||palabra||. Esto sirve para desalentar ver la respuesta de primeras.

También, si se está dentro de una sala de ahorcado:

`{prefix}guess|adivinar <caracter>` para tratar de adivinar un solo caracter de la frase oculta.

`{prefix}display|mostrar` para mostrar de nuevo la pantalla del juego de ahorcado. Ahora esta nueva pantalla será la
que se actualice para mostrar el avance del juego.


*desarrolado por Franco 'NLGS' Lighterman.*
Repositorio: *https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios*
"""

EASTER_EGGS = archivos.cargar_lineas("easter_eggs.txt")
"""
Pequeños guiños escondidos (más o menos).
"""

def existe_unidad(unidad: str, guia: archivos.DiccionarioGuia) -> bool:
    """
    Verifica si la unidad pasada existe dentro de la guía donde se guardan
    los ejercicios.

    Se sobreentiende que todas las claves de la guía son caracteres numéricos,
    y así debería mantenerse porque no se recomienda mutarlo.
    """

    return unidad in [parte for parte in guia.keys()]

def existe_ejercicio(ejercicio: str, unidad: str, guia: archivos.DiccionarioGuia) -> bool:
    """
    Verifica si un determinado ejercicio existe en una determinada unidad.
    """

    if not existe_unidad(unidad, guia):

        return False

    return ejercicio in [ej for ej in guia[unidad].keys()]

def encontrar_meme(id: str, memes: list[str]=EASTER_EGGS) -> str:
    """
    Verifica si una imagen con un 'id' dado se encuentra entre las imágenes
    disponibles. De ser así, le agrega también al link la extensión correspondiente.
    """

    link_sin_tipo = f"https://i.imgur.com/{id}"
    tiene_extension = (lambda ext, img: f"{link_sin_tipo}.{ext}" == img)

    for meme in memes:

        if any([tiene_extension(ext, meme) for ext in ("png", "jpg", "jpeg", "PNG", "JPG", "JPEG")]):

            return meme

    return choice(memes)



bot = custom_bot.CustomBot()
"""
El objeto de tipo 'Bot' que maneja todo el comportamiento.
"""


@bot.event
async def on_ready() -> None:
    """
    El bot se conectó y está listo para usarse.
    """

    print(f"[ {str(datetime.now())} ] ¡{bot.user} conectado y listo para utilizarse!")

async def mandar_dm(ctx: Context, mensaje: str) -> None:
    """
    Manda un mensaje por privado.
    """

    await ctx.author.create_dm()
    await ctx.author.dm_channel.send(mensaje)
    await ctx.message.delete()

@bot.event
async def on_guild_join(guild) -> None:
    """
    El bot se conectó por primera vez a un servidor.
    """

    print(f"El bot se conectó a {guild.name}")

    dic_prefijos = archivos.cargar_pares_valores(custom_bot.PREFIXES_FILE)
    dic_prefijos[str(guild.id)] = custom_bot.DEFAULT_PREFIX

    archivos.guardar_pares_valores(dic_prefijos, custom_bot.PREFIXES_FILE)

    dic_versiones = archivos.cargar_pares_valores(custom_bot.VERSIONS_FILE)
    dic_versiones[str(guild.id)] = custom_bot.DEFAULT_VERSION

    archivos.guardar_pares_valores(dic_versiones, custom_bot.VERSIONS_FILE)

    bot.guias = custom_bot.definir_guias()

@bot.event
async def on_thread_update(before: Thread, after: Thread) -> None:
    """
    Un hilo fue archivado. Si es uno de las partidas de ahorcado, lo elimina.
    """

    partida = bot.encontrar_partida(str(after.id))

    if partida and after.archived:

        bot.partidas.pop(str(after.id))
        await after.parent.send(f"**[AVISO]** Partida `{after.name}` fue eliminada por estar 1 hora inactivo y ser archivado.")
        await after.delete()

@bot.command(name="ej", aliases=["ejercicio", "enunciado"], help="Muestra ejercicios de la guía.")
async def leer_ejercicio(ctx, unidad: str, ejercicio: str, *opciones) -> None:

    guia = bot.guias[str(ctx.guild.id)]

    if not existe_ejercicio(ejercicio, unidad, guia):

        return

    enunciado = guia[unidad][ejercicio]
    mensaje = f"**{ctx.author.mention}** ha consultado:\n\n>>> **Unidad** {unidad} - \"{guia[unidad]['titulo']}\"  |  **Ejercicio** {ejercicio}:\n\n**{unidad}.{ejercicio}.** {enunciado}"

    if "dm" in opciones:

        await mandar_dm(ctx, mensaje)

    else:

        await ctx.channel.send(mensaje)

@bot.command(name="info", help="Muestra una lista de todos los comandos.")
async def mostrar_info(ctx: Context, *opciones):
    """
    Muestra una lista con los comandos y lo que hace cada uno.
    """

    version_guia = bot.guias[str(ctx.guild.id)]["version"]

    if "dm" in opciones:

        await mandar_dm(ctx, INFO_MESSAGE.format(version=version_guia, prefix=ctx.prefix))

    else:

        await ctx.channel.send(INFO_MESSAGE.format(version=version_guia, prefix=ctx.prefix))

@bot.command(name="random", aliases=["aleatorio", 'r'], help="Muestra un ejercicio aleatorio de la guía.")
async def ejercicio_al_azar(ctx, unidad_posible: Optional[str]=None, sentido: str='=', *opciones) -> None:
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

    guia = bot.guias[str(ctx.guild.id)]

    unidad_pivote = (unidad_posible if (unidad_posible and existe_unidad(unidad_posible, guia)) else choice(list(guia.keys())))
    expresion_busqueda = None
    unidad_elegida = ''
    ejercicio_elegido = ''

    if sentido == '=':

        unidad_elegida = unidad_pivote
        ejercicio_elegido = choice([ej for ej in guia[unidad_pivote].keys()])

    elif sentido == '<':

        expresion_busqueda = (lambda u: u < int(unidad_pivote))

    elif sentido == "<=":

        expresion_busqueda = (lambda u: u <= int(unidad_pivote))

    elif sentido == '>':

        expresion_busqueda = (lambda u: u > int(unidad_pivote))

    elif sentido == ">=":

        expresion_busqueda = (lambda u: u >= int(unidad_pivote))

    else: return

    if expresion_busqueda:

        unidad_elegida = choice([unidad for unidad in guia.keys() if expresion_busqueda(int(unidad))])
    
    ejercicio_elegido = choice([ej for ej in guia[unidad_elegida].keys()])

    await leer_ejercicio(ctx, unidad_elegida, ejercicio_elegido, ("dm" if ("dm" in opciones) else ''))

@bot.command(name="prefix", aliases=["prefijo"], help="Cambia el prefijo de los comandos.")
async def cambiar_prefijo(ctx: Context, nuevo_prefijo: str) -> None:
    """
    Cambia el prefijo utilizado para convocar a los comandos, solamente del
    servidor de donde el comando fue escrito.

    Se da por hecho que el servidor ya está memorizado en el diccionario.
    """

    # Si está en el servidor de la materia, que sólo los docente y diego puedan actualizar el prefijo.
    if ctx.guild.id == ALGORITMOS_ESSAYA_ID and all([role.id not in (ROL_DIEGO_ID, ROL_DOCENTE_ID) for role in ctx.author.roles]):

        return

    prefijo_viejo = ctx.prefix

    dic_prefijos = archivos.cargar_pares_valores(custom_bot.PREFIXES_FILE)
    dic_prefijos[str(ctx.guild.id)] = nuevo_prefijo
    archivos.guardar_pares_valores(dic_prefijos, custom_bot.PREFIXES_FILE)

    await ctx.channel.send(f"**[AVISO]** El prefijo de los comandos fue cambiado de `{prefijo_viejo}` a `{nuevo_prefijo}` exitosamente.", delete_after=30)

@bot.command(name="guia", aliases = ["version"], help="Cambia la versión de la guía.")
async def cambiar_version_guia(ctx: Context, nueva_version: str) -> None:
    """
    Cambia la versión de la guía a utilizar, si dicha versión es válida.
    """

    # Si está en el servidor de la materia, que sólo los docente y diego puedan actualizar la versión de la guía.
    if ctx.guild.id == ALGORITMOS_ESSAYA_ID and all([role.id not in (ROL_DIEGO_ID, ROL_DOCENTE_ID) for role in ctx.author.roles]):

        return

    if not archivos.version_es_valida(nueva_version):

        versiones = " - ".join(f"`{version}`" for version in archivos.lista_versiones())

        await ctx.channel.send(f"**[ERROR]** La versión especificada `{nueva_version}` no es válida.\nLas versiones válidas son: {versiones}", delete_after=10)

    else:

        dic_versiones = archivos.cargar_pares_valores(custom_bot.VERSIONS_FILE)

        version_vieja = bot.guias[str(ctx.guild.id)]["version"]
        dic_versiones[str(ctx.guild.id)] = nueva_version
        archivos.guardar_pares_valores(dic_versiones, custom_bot.VERSIONS_FILE)

        await ctx.channel.send(f"**[AVISO]** La versión de la guía fue cambiada de `{version_vieja}` a `{nueva_version}` exitosamente.", delete_after=30)

@bot.command(name="meme", help="Para los curiosos aburridos.")
async def mostrar_meme(ctx: Context, id: Optional[str]=None, *opciones) -> None:
    """
    Muestra una línea al azar del archivo de easter eggs.
    """

    meme = (encontrar_meme(id) if id else choice(EASTER_EGGS))

    if "dm" in opciones or id == "dm":

        await mandar_dm(ctx, meme)

    else:

        await ctx.channel.send(meme)

# Comandos para ahorcado

@bot.command(name="hanged", aliases=["ahorcado"], help="Interactúa con un juego de ahorcado.")
async def crear_sala(ctx: Context, vidas: str='7', *frase) -> None:
    """
    Dependiendo de los comandos que se pasen, interactúa con
    las de juego de ahorcado que hay actualmente.
    """

    if vidas.isdigit():

        await bot.hanged_create(ctx, int(vidas), *frase)

@bot.command(name="guess", aliases=["adivinar"], help="Comando para adivinar una letra en el comando.")
async def adivinar_letra(ctx: Context, letra: str=''):
    """
    Adivina una letra en una partida en curso de ahorcado.
    """

    await bot.hanged_guess(ctx, letra)

    termino, es_victoria = bot.partidas[str(ctx.channel.id)].termino_juego()

    if termino:

        await bot.fin_del_juego(ctx, es_victoria)

@bot.command(name="display", aliases=["mostrar"], help="Muestra la pantalla del juego de ahorcado, por si es muy molesto scrollear.")
async def mostrar_juego(ctx: Context) -> None:
    """
    Muestra el estado actual de un juego de ahorcado, si
    de tantos mensajes es molesto ver la pantalla ya.
    """

    partida = bot.encontrar_partida(str(ctx.channel.id))

    if not partida:

        return

    nuevo_display = await ctx.channel.send(partida)
    partida.definir_display(nuevo_display.id)