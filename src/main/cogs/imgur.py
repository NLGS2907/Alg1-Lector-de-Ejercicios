"""
Cog para comandos del cliente de Imgur.
"""

from random import choice
from typing import TYPE_CHECKING, Optional

from discord import Attachment, Interaction, Message
from discord.app_commands import command as appcommand
from discord.app_commands import describe

from ..constantes import MEMES_ALBUM_NAME
from .general import CogGeneral

if TYPE_CHECKING:

    from ..lector import Lector


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
    async def buscar_meme_en_adjunto(msg: Message) -> Optional[Attachment]:
        """
        Busca si existe un meme en los datos adjunto por el mensaje que
        está ejecutando el comando.
        """

        archivo = None

        if (msg.attachments and
            CogImgur.es_tipo_imagen(CogImgur.tipo_mime(msg.attachments[0].content_type))):

            archivo = msg.attachments[0]

        return archivo


    @staticmethod
    async def buscar_meme_en_referencia(ctx: Interaction) -> Optional[Attachment]:
        """
        Busca si existe un meme en un mensaje referenciado por el que está
        ejecutando el comando.
        """

        archivo = None

        referencia = ctx.message.reference

        if referencia:

            archivo = await CogImgur.buscar_meme_en_adjunto(
                      await ctx.fetch_message(referencia.message_id))

        return archivo


    def es_numero_meme_valido(self,
                              indice_meme: int,
                              lista_memes: list[str]) -> bool:
        """
        Verifica si el índice que se pasó por parámetro es válido o no. En caso
        de no serlo envía un mensaje indicándolo.
        """

        limite_memes = len(lista_memes)

        return all((lista_memes, indice_meme > 0, indice_meme <= limite_memes))


    @appcommand(name="meme",
                description="Para los curiosos.")
    @describe(numero="El índice específico del meme que se quiere.")
    async def mostrar_meme(self,
                           interaction: Interaction,
                           numero: Optional[int]=None) -> None:
        """
        Muestra un meme o lo agrega al album donde estan guardados.
        """

        await interaction.response.defer()

        memes = self.bot.cliente_imgur.get_links_imagenes(MEMES_ALBUM_NAME)
        meme_link = None

        if numero is None:
            meme_link = choice(memes)

        elif self.es_numero_meme_valido(numero, memes):
            meme_link = memes[numero - 1]

        else:
            self.bot.log.error(f"Número de Meme '{numero}' inválido")
            await interaction.followup.send(content="**[ERROR]** El número de meme " +
                                            f"`{numero}` ingresado no es válido.\n\n" +
                                            "Las opciones disponibles incluyen de `1` " +
                                            f"a `{len(memes)}`.")
            return

        await interaction.followup.send(content=meme_link)


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogImgur(bot))
