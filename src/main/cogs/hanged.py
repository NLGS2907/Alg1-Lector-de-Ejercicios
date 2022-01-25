"""
Cog para comandos del ahorcado.
"""

from discord.ext.commands import command, Context

from .general import CogGeneral


class CogHanged(CogGeneral):
    """
    Cog para comandos relacionados al ahorcado.
    """

    @command(name="hanged", aliases=["ahorcado"], usage="<vidas> <*frase>", help="Interactúa con un juego de ahorcado.")
    async def crear_sala(self, ctx: Context, vidas: str='7', *frase) -> None:
        """
        Dependiendo de los comandos que se pasen, interactúa con
        las de juego de ahorcado que hay actualmente.
        """

        if vidas.isdigit():

            await self.bot.hanged_create(ctx, int(vidas), *frase)


    @command(name="guess", aliases=["adivinar"], usage="<caracter>", help="Comando para adivinar una letra en el comando.")
    async def adivinar_letra(self, ctx: Context, letra: str=''):
        """
        Adivina una letra en una partida en curso de ahorcado.
        """

        await self.bot.hanged_guess(ctx, letra)

        termino, es_victoria = self.bot.partidas[str(ctx.channel.id)].termino_juego()

        if termino:

            await self.bot.fin_del_juego(ctx, es_victoria)


    @command(name="display", aliases=["mostrar"], help="Muestra la pantalla del juego de ahorcado, por si es muy molesto scrollear.")
    async def mostrar_juego(self, ctx: Context) -> None:
        """
        Muestra el estado actual de un juego de ahorcado, si
        de tantos mensajes es molesto ver la pantalla ya.
        """

        partida = self.bot.encontrar_partida(str(ctx.channel.id))

        if not partida:

            return

        nuevo_display = await ctx.channel.send(str(partida))
        partida.definir_display(nuevo_display.id)