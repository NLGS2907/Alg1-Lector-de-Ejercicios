"""
Cog para comandos del cliente de Imgur.
"""

from typing import Optional
from discord import Attachment, Message
from discord.ext.commands import command, Context
from random import choice
from os import remove as dir_remove
import datetime

from .general import CogGeneral
from ..logger.logger import log
from ..auxiliar.auxiliar import mandar_dm

from ..constantes.constantes import DATE_FORMAT, MEMES_ALBUM_NAME


class CogImgur(CogGeneral):
    """
    Cog para comandos con el cliente de Imgur.
    """

    @staticmethod
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


    @staticmethod
    def es_tipo_imagen(mime_type: tuple[str]) -> bool:
        """
        Devuelve 'True' si el string pasado por parametro es del formato
        de un tipo MIME, y si este es de tipo 'image'. De lo contrario,
        devuelve 'False'.
        """

        return mime_type[0] == "image"


    @staticmethod
    async def es_numero_meme_valido(mensaje_enviado: Message, indice_meme: int, lista_memes: list[str]) -> bool:
        """
        Verifica si el índice que se pasó por parámetro es válido o no. En caso
        de no serlo envía un mensaje indicándolo.
        """

        limite_memes = len(lista_memes)

        if all((lista_memes, indice_meme > 0, indice_meme <= limite_memes)):

            return True

        await mensaje_enviado.edit(f"**[ERROR]** El número de meme `{indice_meme}` ingresado no es válido.\n\nLas opciones disponibles incluyen de `1` a `{limite_memes}`.")
        return False


    @staticmethod
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


    @staticmethod
    async def buscar_meme_en_adjunto(msg: Message) -> Optional[Attachment]:
        """
        Busca si existe un meme en los datos adjunto por el mensaje que
        está ejecutando el comando.
        """

        archivo = None

        if msg.attachments and CogImgur.es_tipo_imagen(CogImgur.tipo_mime(msg.attachments[0].content_type)):

            archivo = msg.attachments[0]

        return archivo


    @staticmethod
    async def buscar_meme_en_referencia(ctx: Context) -> Optional[Attachment]:
        """
        Busca si existe un meme en un mensaje referenciado por el que está
        ejecutando el comando.
        """

        archivo = None

        referencia = ctx.message.reference

        if referencia:

            archivo = await CogImgur.buscar_meme_en_adjunto(await ctx.fetch_message(referencia.message_id))

        return archivo


    @staticmethod
    async def subir_meme(ctx: Context) -> None:
        """
        Trata de subir efectivamente el meme si lo encuentra.
        """

        adjunto_meme = await CogImgur.buscar_meme_en_adjunto(ctx.message)

        if not adjunto_meme:

            adjunto_meme = await CogImgur.buscar_meme_en_referencia(ctx)

        if not adjunto_meme:

            await ctx.channel.send("**[ERROR]** No se ha encontrado ningún meme.", delete_after=10)
            return

        mensaje_enviado = await ctx.channel.send("Subiendo Meme...", reference=ctx.message.to_reference())

        meme_dir = f"temp/{str(datetime.now().strftime(DATE_FORMAT))}.{CogImgur.tipo_mime(adjunto_meme.content_type)[1]}"
        album_destino = ctx.bot.cliente.get_album_por_nombre(MEMES_ALBUM_NAME)
        numero_meme = ctx.bot.cliente.cuantas_imagenes(MEMES_ALBUM_NAME)
        meme_titulo = f"Meme No. {numero_meme + 1}"

        log.info(f"Guardando archivo temporalmente en '{meme_dir}'")
        await adjunto_meme.save(meme_dir)
        log.info("¡Guardado!")

        ctx.bot.cliente.image_upload(meme_dir, meme_titulo, f"Este es el {meme_titulo}", album=album_destino["id"])
        log.info(f"Meme '{meme_titulo}' subido exitosamente")

        try:

            dir_remove(meme_dir)
            log.info(f"Se borró el archivo en '{meme_dir}'")

        except:

            log.warning(f"No se pudo borrar el archivo en '{meme_dir}'")

        await mensaje_enviado.edit(content=f"¡De acuerdo, {ctx.author.mention}! Ya guardé esa imagen.\nAhora este es el nuevo Meme No. `{numero_meme}`.", delete_after=15)


    @command(name="meme", usage="-add|-agregar|<numero>", help="Para los curiosos aburridos.")
    async def mostrar_meme(self, ctx: Context, *opciones) -> None:
        """
        Muestra un meme o lo agrega al album donde estan guardados.
        """

        if "-add" in opciones or "-agregar" in opciones:

            await self.subir_meme(ctx)

        else:

            status = "**[AVISO]** Cargando meme..."

            if "-dm" in opciones:

                mensaje_enviado = await mandar_dm(ctx, status)

            else:

                mensaje_enviado = await ctx.channel.send(status)

            numero = CogImgur.hay_valor_numerico(opciones)
            memes = self.bot.cliente.get_links_imagenes(MEMES_ALBUM_NAME)
            meme_link = None

            if numero:
            
                if await CogImgur.es_numero_meme_valido(mensaje_enviado, numero, memes):

                    meme_link = memes[numero - 1]

            else:

                meme_link = choice(memes)

            if meme_link: await mensaje_enviado.edit(meme_link)