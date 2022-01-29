"""
Módulo para funciones auxiliares
"""

from typing import Optional

from discord import Embed, Message
from discord.ext.commands import Bot, Context
from discord.ui import View

from ..archivos.archivos import cargar_json
from ..constantes.constantes import (ALGORITMOS_ESSAYA_ID, DEFAULT_PREFIX,
                                     PROPERTIES_PATH, ROL_DIEGO_ID,
                                     ROL_DOCENTE_ID)


def es_rol_valido(ctx: Context) -> bool:
    """
    Verifica si está en el servidor del curso, y si es así,
    si se tienen los roles correspondientes.
    """

    return not all((ctx.guild.id == ALGORITMOS_ESSAYA_ID,
               all([role.id not in (ROL_DIEGO_ID, ROL_DOCENTE_ID) for role in ctx.author.roles])))


async def mandar_dm(ctx: Context,
                    contenido: Optional[str]=None,
                    vista: Optional[View]=None,
                    embed: Optional[Embed]=None) -> None:
    """
    Manda un mensaje por privado.
    """

    await ctx.author.create_dm()
    mensaje_enviado = await ctx.author.dm_channel.send(content=contenido, view=vista, embed=embed)
    vista.msg = mensaje_enviado
    await ctx.message.delete()


def get_prefijo(_bot: Bot, mensaje: Message) -> str:
    """
    Se fija en el diccionario de prefijos y devuelve el que
    corresponda al servidor de donde se convoca el comando.
    """

    return cargar_json(PROPERTIES_PATH)["prefijos"].get(str(mensaje.guild.id), DEFAULT_PREFIX)