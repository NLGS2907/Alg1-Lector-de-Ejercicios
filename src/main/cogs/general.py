"""
Cog general para uso de herencia.
"""

from traceback import format_exc
from typing import TYPE_CHECKING, Any, Optional, Union

from discord import Interaction
from discord.app_commands import AppCommandError, Group
from discord.ext.commands import Cog, Context
from discord.utils import MISSING

if TYPE_CHECKING:

    from discord import Permissions
    from discord.app_commands import locale_str

    from ..lector import Lector

class GrupoGeneral(Group):
    """
    Grupo general para que se herede de él.
    """

    def __init__(self,
                 bot: "Lector",
                 *,
                 name: Union[str, "locale_str"] = MISSING,
                 description: Union[str, "locale_str"] = MISSING,
                 parent: Optional[Group] = None,
                 guild_ids: Optional[list[int]] = None,
                 guild_only: bool = MISSING,
                 nsfw: bool = MISSING,
                 auto_locale_strings: bool = True,
                 default_permissions: Optional["Permissions"] = MISSING,
                 extras: dict[Any, Any] = MISSING) -> None:
        """
        Inicializa una instancia de '_GrupoABC', o una hija.
        """

        super().__init__(name=name,
                         description=description,
                         parent=parent,
                         guild_ids=guild_ids,
                         guild_only=guild_only,
                         nsfw=nsfw,
                         auto_locale_strings=auto_locale_strings,
                         default_permissions=default_permissions,
                         extras=extras)
        self.bot: "Lector" = bot


GroupsList = list[type[GrupoGeneral]]

class CogGeneral(Cog):
    """
    Cog General, para que se herede de él.
    """

    def __init__(self, bot: "Lector") -> None:
        """
        Inicializa una instancia de 'CogGeneral'.
        """

        self.bot: "Lector" = bot
        self._cargar_grupos()


    def _cargar_grupos(self) -> None:
        """
        Carga todos los grupos que tiene registrados el cog.
        """

        for clase_grupo in self.grupos():
            self.bot.tree.add_command(clase_grupo(self.bot))


    @classmethod
    def grupos(cls) -> GroupsList:
        """
        Devuelve la lista de grupos asociados a este Cog.
        """

        return []


    async def cog_app_command_error(self,
                                    interaccion: Interaction,
                                    _error: AppCommandError) -> None:
        """
        Maneja un error de forma predeterminada para todos los cogs.
        """

        await interaccion.response.send_message(f"**[ERROR]** Parece que hubo un error.",
                                                ephemeral=True)
        error_bello = "\n\t|\t".join(f"Excepción en app_commands lanzada:\n{format_exc()}".split("\n"))
        self.bot.log.error(error_bello)


    async def cog_before_invoke(self, ctx: Context) -> None:
        """
        Registra en el log el comando siendo procesado.
        """

        hay_guild = ("" if ctx.guild is None else f" en {ctx.guild.name!r}")
        hay_mensaje = ("un mensaje sin contenido" if not ctx.message.content else f"el mensaje {ctx.message.content!r}")
        self.bot.log.info((f"[CMD] {ctx.author.name!r} está tratando de ejecutar el comando " +
                           f"{ctx.command.name!r}{hay_guild}, mediante {hay_mensaje}."))


    async def cog_after_invoke(self, ctx: Context) -> None:
        """
        Registra en el log el comando procesado.
        """

        hay_guild = ("" if ctx.guild is None else f" en {ctx.guild.name!r}")
        hay_mensaje = ("un mensaje sin contenido" if not ctx.message.content else f"el mensaje {ctx.message.content!r}")
        self.bot.log.info((f"[CMD] {ctx.author.name!r} ejecutó el comando " +
                           f"{ctx.command.name!r}{hay_guild}, mediante {hay_mensaje}."))


async def setup(_bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    ... # Este Cog no está pensado para agregarse.
