"""
Módulo dedicado a contener al comportamiento del bot.
"""

from typing import Optional
from random import choice
from os import remove
from time import sleep

from discord import Thread, Guild, Game, Message, Attachment, Interaction
from discord.ext.commands import Context, check, is_owner
from discord.ui import View
from datetime import datetime

import custom_bot
from custom_bot import log

import cliente_imgur
import interfaces
import archivos
import ppt

from constantes import ALGORITMOS_ESSAYA_ID, INFO_MESSAGE, MESSAGE_FORMAT, ROL_DIEGO_ID, ROL_DOCENTE_ID, WHATSNEW, elegir_frases

# Para que no tire error en Windows al cerrar el Bot.

from platform import system
from asyncio import set_event_loop_policy

try:

    from asyncio import WindowsSelectorEventLoopPolicy

    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())

except ImportError:

    log.warning("No se pudo importar 'WindowsSelectorEventLoopPolicy', probablemente porque esto no es Windows.")


def existe_unidad(unidad: str, guia: archivos.DiccionarioGuia) -> bool:
    """
    Verifica si la unidad pasada existe dentro de la guía donde se guardan
    los ejercicios.

    Se sobreentiende que todas las claves de la guía son caracteres numéricos,
    y así debería mantenerse porque no se recomienda mutarlo.
    """

    return unidad in [parte for parte in guia.keys()]


def existe_ejercicio(ejercicio: str, unidad: str, guia: archivos.DiccionarioGuia) -> tuple[bool, bool]:
    """
    Verifica si un determinado ejercicio existe en una determinada unidad.

    Devuelve uan tupla donde el primer elemento indica si existe la unidad
    especificada, mientras que el segundo especifica si existe el ejercicio
    especificado. Si no existe la unidad, tampoco el ejercicio.
    """

    if not existe_unidad(unidad, guia):

        return False, False

    return True, ejercicio in [ej for ej in guia[unidad].keys()]


async def mostrar_unidad_y_ejercicio_validos(ctx: Context, unidad: Optional[str]=None, ejercicio: Optional[str]=None) -> bool:
    """
    Muestra por pantalla errores que le indican al usuario si los valores
    ingresados para la unidad y el ejercicio son inválidos.
    """

    guia = bot.guias[str(ctx.guild.id)]

    unidad_existe, ej_existe = existe_ejercicio(ejercicio, unidad, guia)

    if not unidad_existe:

        if unidad is None:

            await ctx.channel.send(content="Por favor elija el número de unidad", view=interfaces.SelectorUnidad(guia=guia))

        else:

            unidades = archivos.lista_unidades(guia)

            await ctx.channel.send(f"**[ERROR]** El número de unidad `{unidad}` no es válido. Los valores aceptados son:\n\n{' - '.join([f'`{u}`' for u in unidades])}")

        return False

    elif not ej_existe:

        if ejercicio is None:

            await ctx.channel.send(content="Por favor elija un ejercicio", view=interfaces.SelectorEjercicios(guia=guia, unidad=unidad))

        else:

            ejercicios = archivos.lista_ejercicios(guia, unidad)

            await ctx.channel.send(f"**[ERROR]** El número de ejercicio `{ejercicio}` no es válido. Los valores aceptados son:\n\n{' - '.join([f'`{ej}`' for ej in ejercicios])}")

        return False

    return True


def tipo_mime(str_mime: str) -> Optional[tuple[str]]:
    """
    Transforma un string 'tipo/subtipo' en una tupla
    '(tipo, subtipo)', si el formato del string es válido.
    Si no, devuelve 'None'.
    """

    tupla_a_devolver = None
    
    tupla_mime = str_mime.split('/')

    if len(tupla_mime) == 2 and tupla_mime[0] and tupla_mime[1]:

        tupla_a_devolver = tupla_mime

    return tupla_a_devolver


def es_tipo_imagen(mime_type: tuple[str]) -> bool:
    """
    Devuelve 'True' si el string pasado por parametro es del formato
    de un tipo MIME, y si este es de tipo 'image'. De lo contrario,
    devuelve 'False'.
    """

    return mime_type[0] == "image"


def hay_valor_numerico(lista: list[str]) -> Optional[int]:
    """
    Busca en una lista si hay un números en tipo 'string'.
    De ser así, devuelve el primer caso encontrado, ya
    convertido a tipo 'int'.
    """

    elemento_a_devolver = None

    for elem in lista:

        try:
            
            elemento_a_devolver = int(elem)
            break

        except ValueError:

            continue

    return elemento_a_devolver


# --------------------------------------------------#
#               Instanciación del Bot               #
# --------------------------------------------------#

actividad_bot = Game(name="!info")

bot = custom_bot.CustomBot(actividad=actividad_bot)
"""
El objeto de tipo 'Bot' que maneja todo el comportamiento.
"""

cliente = cliente_imgur.MemeImgur()
"""
El cliente de Imgur encargado de manejar las imágenes que pide el bot.
"""


def es_rol_valido(ctx: Context) -> bool:
    """
    Verifica si está en el servidor del curso, y si es así,
    si se tienen los roles correspondientes.
    """

    return not all((ctx.guild.id == ALGORITMOS_ESSAYA_ID,
                   all([role.id not in (ROL_DIEGO_ID, ROL_DOCENTE_ID) for role in ctx.author.roles])))


async def mandar_dm(ctx: Context, mensaje: str, vista: View) -> None:
    """
    Manda un mensaje por privado.
    """

    await ctx.author.create_dm()
    await ctx.author.dm_channel.send(content=mensaje, view=vista)
    await ctx.message.delete()


def es_ultimo_mensaje(msg: Message) -> bool:
    """
    Verifica que el mensaje a procesar no sea el
    ultimo del canal.
    """

    return msg == msg.channel.last_message


def es_mensaje_de_bot(msg: Message) -> bool:
    """
    Verifica si un mensaje pasado es un mensaje escrito
    por el bot.
    """

    return not es_ultimo_mensaje(msg) and msg.author == bot.user


def es_mensaje_comando(msg: Message) -> bool:
    """
    Verifica si un mensaje escrito por un usuario o
    bot es un comando.
    """

    return (not es_ultimo_mensaje(msg) and msg.content.startswith(custom_bot.get_prefijo(bot, msg))) or es_mensaje_de_bot(msg)


async def buscar_meme_en_adjunto(msg: Message) -> Optional[Attachment]:
    """
    Busca si existe un meme en los datos adjunto por el mensaje que
    está ejecutando el comando.
    """

    archivo = None

    if msg.attachments and es_tipo_imagen(tipo_mime(msg.attachments[0].content_type)):

        archivo = msg.attachments[0]

    return archivo


async def buscar_meme_en_referencia(ctx: Context) -> Optional[Attachment]:
    """
    Busca si existe un meme en un mensaje referenciado por el que está
    ejecutando el comando.
    """

    archivo = None

    referencia = ctx.message.reference

    if referencia:

        archivo = await buscar_meme_en_adjunto(await ctx.fetch_message(referencia.message_id))

    return archivo


async def es_numero_meme_valido(mensaje_enviado: Message, indice_meme: int, lista_memes: list[str]) -> bool:
    """
    Verifica si el índice que se pasó por parámetro es válido o no. En caso
    de no serlo envía un mensaje indicándolo.
    """

    limite_memes = len(lista_memes)

    if all((lista_memes, indice_meme > 0, indice_meme < limite_memes)):

        return True

    await mensaje_enviado.edit(f"**[ERROR]** El número de meme `{indice_meme}` ingresado no es válido.\n\nLas opciones disponibles incluyen de `1` a `{limite_memes}`.")
    return False

@bot.event
async def on_ready() -> None:
    """
    El bot se conectó y está listo para usarse.
    """

    log.info(f"¡{bot.user} conectado y listo para utilizarse!")

@bot.event
async def on_command(ctx: Context):
    """
    El usuario está tratando de invocar un comando.
    """

    log.info(f"El usuario {ctx.author} está tratando de invocar '{ctx.command}' en el canal '#{ctx.channel.name}' del server '{ctx.guild.name}' mediante el mensaje '{ctx.message.content}'")

@bot.event
async def on_command_completion(ctx: Context):
    """
    El usuario ejecutó el comando satisfactoriamente.
    """

    log.info(f"{ctx.author} ha invocado '{ctx.command}' satisfactoriamente")


@bot.event
async def on_guild_join(guild: Guild) -> None:
    """
    El bot se conectó por primera vez a un servidor.
    """

    log.info(f"El bot se conectó a '{guild.name}'")

    dic_prefijos = archivos.cargar_pares_valores(custom_bot.PREFIXES_PATH)
    dic_prefijos[str(guild.id)] = custom_bot.DEFAULT_PREFIX

    archivos.guardar_pares_valores(dic_prefijos, custom_bot.PREFIXES_PATH)

    dic_versiones = archivos.cargar_pares_valores(custom_bot.VERSIONS_PATH)
    dic_versiones[str(guild.id)] = custom_bot.DEFAULT_VERSION

    archivos.guardar_pares_valores(dic_versiones, custom_bot.VERSIONS_PATH)

    bot.guias = custom_bot.definir_guias()


@bot.event
async def on_thread_update(before: Thread, after: Thread) -> None:
    """
    Un hilo fue actualizado. Si esta actualización fue que el hilo en
    cuestión fue archivado, y si es uno de las partidas de ahorcado,
    lo elimina.
    """

    partida = bot.encontrar_partida(str(after.id))

    if partida and after.archived:

        bot.partidas.pop(str(after.id))
        await after.parent.send(f"**[AVISO]** Partida `{after.name}` fue eliminada al ser archivado (probablemente por la hora de inactividad).")
        await after.delete()


@bot.command(name="info", aliases=["i"], usage="-dm", help="Muestra una lista de todos los comandos.")
async def mostrar_info(ctx: Context, *opciones):
    """
    Muestra una lista con los comandos y lo que hace cada uno.
    """

    version_guia = bot.guias[str(ctx.guild.id)]["version"]
    info_ui = interfaces.InfoUI()

    if "-dm" in opciones:

        await mandar_dm(ctx, INFO_MESSAGE['1'].format(version_bot=bot.version, version=version_guia, prefix=ctx.prefix), view=info_ui)

    else:

        await ctx.channel.send(INFO_MESSAGE['1'].format(version_bot=bot.version, version=version_guia, prefix=ctx.prefix), view=info_ui)


@bot.command(name="ej", aliases=["ejercicio", "enunciado"], usage="<unidad> <ejercicio> -dm", help="Muestra ejercicios de la guía.")
async def leer_ejercicio(ctx: Context, unidad: Optional[str]=None, ejercicio: Optional[str]=None, *opciones) -> None:

    guia = bot.guias[str(ctx.guild.id)]

    if not await mostrar_unidad_y_ejercicio_validos(ctx, unidad, ejercicio):

        return

    enunciado = guia[unidad][ejercicio]

    mensaje = MESSAGE_FORMAT.format(mention=ctx.author.mention, unidad=unidad, titulo=guia[unidad]["titulo"], ejercicio=ejercicio, enunciado=enunciado)

    interfaz = interfaces.NavegadorEjercicios(guia=guia, unidad=unidad, ejercicio=ejercicio)

    if "-dm" in opciones:

        await mandar_dm(ctx, mensaje, vista=interfaz)

    else:

        await ctx.channel.send(mensaje, view=interfaz)


@bot.command(name="random", aliases=["aleatorio", 'r'], usage="<unidad posible>, <sentido> -dm", help="Muestra un ejercicio aleatorio de la guía.")
async def ejercicio_al_azar(ctx: Context, unidad_posible: Optional[str]=None, sentido: str='=', *opciones) -> None:
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

    match sentido:

        case '=':

            unidad_elegida = unidad_pivote
            ejercicio_elegido = choice([ej for ej in guia[unidad_pivote].keys()])

        case '<':

            expresion_busqueda = (lambda u: u < int(unidad_pivote))

        case "<=":

            expresion_busqueda = (lambda u: u <= int(unidad_pivote))

        case '>':

            expresion_busqueda = (lambda u: u > int(unidad_pivote))

        case ">=":

            expresion_busqueda = (lambda u: u >= int(unidad_pivote))

        case _: return

    if expresion_busqueda:

        unidad_elegida = choice([unidad for unidad in list(guia.keys())[1:] if expresion_busqueda(int(unidad))])
    
    ejercicio_elegido = choice([ej for ej in guia[unidad_elegida].keys()])

    await leer_ejercicio(ctx, unidad_elegida, ejercicio_elegido, ("-dm" if ("-dm" in opciones) else ''))


@bot.command(name="prefix", aliases=["prefijo", "pfx", "px"], usage="<nuevo_prefijo>", help="Cambia el prefijo de los comandos.")
@check(es_rol_valido)
async def cambiar_prefijo(ctx: Context, nuevo_prefijo: str) -> None:
    """
    Cambia el prefijo utilizado para convocar a los comandos, solamente del
    servidor de donde el comando fue escrito.

    Se da por hecho que el servidor ya está memorizado en el diccionario.
    """

    prefijo_viejo = ctx.prefix

    dic_prefijos = archivos.cargar_pares_valores(custom_bot.PREFIXES_PATH)
    dic_prefijos[str(ctx.guild.id)] = nuevo_prefijo
    archivos.guardar_pares_valores(dic_prefijos, custom_bot.PREFIXES_PATH)

    await ctx.channel.send(f"**[AVISO]** El prefijo de los comandos fue cambiado de `{prefijo_viejo}` a `{nuevo_prefijo}` exitosamente.", delete_after=30)
    log.info(f"El prefijo de comandos en '{ctx.guild.name}' fue cambiado de '{prefijo_viejo}' a '{nuevo_prefijo}'")


@bot.command(name="guia", aliases=["guia_version", "gver"], usage="<nueva_version>", help="Cambia la versión de la guía.")
@check(es_rol_valido)
async def cambiar_version_guia(ctx: Context, nueva_version: Optional[str]=None) -> None:
    """
    Cambia la versión de la guía a utilizar, si dicha versión es válida.
    """

    versiones = " - ".join(f"`{version}`" for version in archivos.lista_versiones())

    if nueva_version is not None and not archivos.version_es_valida(nueva_version):

        await ctx.channel.send(f"**[ERROR]** La versión especificada `{nueva_version}` no es válida.\nLas versiones válidas son:\n{versiones}", delete_after=10)
        return

    version_vieja = bot.guias[str(ctx.guild.id)]["version"]

    if not nueva_version:

        await ctx.channel.send(f"Por favor seleccione una versión de la guía", view=interfaces.SelectorGuia(version_actual=version_vieja))

    else:

        archivos.actualizar_guia(nueva_version, str(ctx.guild.id))
        await ctx.channel.send(f"**[AVISO]** La versión de la guía fue cambiada de `{version_vieja}` a `{nueva_version}` exitosamente.", delete_after=30)

    bot.actualizar_guia()

    log.info(f"La versión de la guía en '{ctx.guild.name}' fue cambiada de '{version_vieja}' a '{nueva_version}'")


@bot.command(name="meme", usage="-add|-agregar|<numero>", help="Para los curiosos aburridos.")
async def mostrar_meme(ctx: Context, *opciones) -> None:
    """
    Muestra un meme o lo agrega al album donde estan guardados.
    """

    if "-add" in opciones or "-agregar" in opciones:

        await subir_meme(ctx)

    else:

        status = "**[AVISO]** Cargando meme..."

        if "-dm" in opciones:

            mensaje_enviado = await mandar_dm(ctx, status)

        else:

            mensaje_enviado = await ctx.channel.send(status, delete_after=120)

        numero = hay_valor_numerico(opciones)
        memes = cliente.get_links_imagenes(cliente_imgur.MEMES_ALBUM_NAME)
        meme_link = None

        if numero:
        
            if await es_numero_meme_valido(mensaje_enviado, numero, memes):

                meme_link = memes[numero - 1]

        else:

            meme_link = choice(memes)

        if meme_link: await mensaje_enviado.edit(meme_link)


async def subir_meme(ctx: Context) -> None:
    """
    Trata de subir efectivamente el meme si lo encuentra.
    """

    adjunto_meme = await buscar_meme_en_adjunto(ctx.message)

    if not adjunto_meme:

        adjunto_meme = await buscar_meme_en_referencia(ctx)

    if not adjunto_meme:

        await ctx.channel.send("**[ERROR]** No se ha encontrado ningún meme.", delete_after=10)
        return

    mensaje_enviado = await ctx.channel.send("Subiendo Meme...", reference=ctx.message.to_reference())

    meme_dir = f"temp/{str(datetime.now().strftime(custom_bot.DATE_FORMAT))}.{tipo_mime(adjunto_meme.content_type)[1]}"
    album_destino = cliente.get_album_por_nombre(cliente_imgur.MEMES_ALBUM_NAME)
    numero_meme = cliente.cuantas_imagenes(cliente_imgur.MEMES_ALBUM_NAME)
    meme_titulo = f"Meme No. {numero_meme + 1}"

    log.info(f"Guardando archivo temporalmente en '{meme_dir}'")
    await adjunto_meme.save(meme_dir)
    log.info("¡Guardado!")

    cliente.image_upload(meme_dir, meme_titulo, f"Este es el {meme_titulo}", album=album_destino["id"])
    log.info(f"Meme '{meme_titulo}' subido exitosamente")

    try:

        remove(meme_dir)
        log.info(f"Se borró el archivo en '{meme_dir}'")

    except:

        log.warning(f"No se pudo borrar el archivo en '{meme_dir}'")

    await mensaje_enviado.edit(content=f"¡De acuerdo, {ctx.author.mention}! Ya guardé esa imagen.\nAhora este es el nuevo Meme No. `{numero_meme}`.", delete_after=15)


# Comandos para ahorcado

@bot.command(name="hanged", aliases=["ahorcado"], usage="<vidas> <*frase>", help="Interactúa con un juego de ahorcado.")
async def crear_sala(ctx: Context, vidas: str='7', *frase) -> None:
    """
    Dependiendo de los comandos que se pasen, interactúa con
    las de juego de ahorcado que hay actualmente.
    """

    if vidas.isdigit():

        await bot.hanged_create(ctx, int(vidas), *frase)


@bot.command(name="guess", aliases=["adivinar"], usage="<caracter>", help="Comando para adivinar una letra en el comando.")
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

    nuevo_display = await ctx.channel.send(str(partida))
    partida.definir_display(nuevo_display.id)


@bot.command(name="clear", aliases=["clean", "cls"], usage="<limite> | -full", help="Limpia el canal de mensajes del bot.")
@check(es_rol_valido)
async def limpiar_mensajes(ctx: Context, limite: int=10, *opciones) -> None:
    """
    Limpia los mensajes del bot del canal de donde se
    invoca el comando.

    Si 'full' está entre las opciones, también borra los
    mensajes de los usuarios que invocan los comandos.
    """

    funcion_check = (es_mensaje_comando if "-full" in opciones else es_mensaje_de_bot)
    eliminados = await ctx.channel.purge(limit=limite + 1, check=funcion_check)

    log.info(f"{len(eliminados)} mensajes fueron eliminados de '#{ctx.channel.name}' en '{ctx.guild.name}'")


@bot.command(name="version", aliases=["ver"], help="Muestra la versión del bot.")
async def mostrar_version(ctx: Context, *opciones) -> None:
    """
    Muestra en el chat la versión actual del bot.
    """

    mensaje = f"Mi versión actual es la `{bot.version}`"

    if "-dm" in opciones:

        await mandar_dm(ctx, mensaje)

    else:

        await ctx.channel.send(mensaje)


@bot.command(name="shutdown", aliases=["shut", "exit", "quit", "salir"], help="Apaga el bot. Uso exclusivo del dev.", hidden=True)
@is_owner()
async def shutdown(ctx: Context) -> None:
    """
    Apaga el bot y lo desconecta.
    """

    await ctx.channel.send(f"**[AVISO]** Cerrando Bot...")

    await ctx.bot.close()

@bot.command(name="flush", aliases=["logclear"], help="Vacía el archivo de registro. Uso exclusivo del dev.", hidden=True)
@is_owner()
async def logflush(ctx: Context):
    """
    Vacía el contenido del archivo de registro.
    """

    with open(custom_bot.LOG_PATH, mode='w'):

        await ctx.channel.send(f"**[AVISO]** Vaciando archivo en '{custom_bot.LOG_PATH}'...", delete_after=10)

@bot.command(name="whatsnew", aliases=["quehaydenuevo", "nuevo"], help="Muestra las novedades de la versión actual.", hidden=True)
async def mostrar_novedades(ctx: Context):
    """
    Muestra las novedades de la versión más nueva del bot.
    """

    await ctx.channel.send(content=WHATSNEW)


@bot.command(name="rps", aliases=["ppt"], help="Hace un pequeño juego de piedra-papel-tijeras.", hidden=True)
async def jugar_ppt(ctx: Context, eleccion: Optional[str]=None) -> None:
    """
    Simula un pequeño juego de 'piedra, papel o tijeras'.
    """

    opciones = ("PIEDRA", "PAPEL", "TIJERAS")
    piedra, papel, tijeras = opciones

    if eleccion == "-reset":

        bot.rps_stats[str(ctx.author.id)] = [0, 0, 0]
        archivos.guardar_stats_ppt(bot.rps_stats)

        await ctx.channel.send(f"¡De acuerdo, {ctx.author.mention}! Ya reseté tus estadísticas a `0` - `0` - `0`. *Imagino no querrá que vean que pierde tanto...*")
        return

    if not eleccion:

        await ctx.channel.send(content=f"{elegir_frases()}\n\n**¡Elige!** ¿Piedra, Papel o Tijeras?\n", reference=ctx.message.to_reference(), view=interfaces.JuegoPPT(stats=bot.rps_stats))
        return

    if eleccion.upper() not in opciones:

        await ctx.channel.send(f"**[ERROR]** Capo, tenés que elegir entre `{piedra}`, `{papel}` o `{tijeras}`.", reference=ctx.message.to_reference())
        return

    await ppt.jugar_partida_ppt(eleccion, ctx.message, bot.rps_stats)
