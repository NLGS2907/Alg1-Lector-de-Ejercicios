"""
Cog para comandos de Piedra, Papel o Tijeras.
"""

from random import choices
from typing import Optional

from discord.ext.commands import Context, command

from ..archivos.archivos import cargar_json, guardar_json
from ..constantes.constantes import PROPERTIES_PATH, RPS_PHRASES
from ..interfaces.ui_ppt import JuegoPPT
from ..ppt.ppt import jugar_partida_ppt
from .general import CogGeneral


class CogRPS(CogGeneral):
    """
    Cog para comandos relacionados al Piedra, Papel o Tijeras.
    """

    @staticmethod
    def elegir_frases(opciones: list[str]) -> str:
        """
        Elige con distinta probabilidad las opciones
        """

        num_opciones = len(opciones)

        pesos = ([10] * (num_opciones - 1) if num_opciones > 1 else []) + [1]

        return ''.join(choices(opciones, weights=pesos))


    @command(name="rps",
             aliases=["ppt"],
             usage="[PIEDRA | PAPEL | TIJERAS | -reset | -stats]",
             help="Hace un pequeño juego de piedra-papel-tijeras.",
             hidden=True)
    async def jugar_ppt(self, ctx: Context, eleccion: Optional[str]=None) -> None:
        """
        Simula un pequeño juego de 'piedra, papel o tijeras'.
        """

        opciones = ("PIEDRA", "PAPEL", "TIJERAS")
        piedra, papel, tijeras = opciones

        match eleccion:

            case "-reset":

                self.bot.rps_stats[str(ctx.author.id)] = [0, 0, 0]
                propiedades = cargar_json(PROPERTIES_PATH)
                propiedades["stats_ppt"] = self.bot.rps_stats
                guardar_json(propiedades, PROPERTIES_PATH)

                await ctx.channel.send(f"¡De acuerdo, {ctx.author.mention}! Ya reseté tus " +
                "estadísticas a `0` - `0` - `0`.\n\n" +
                "*Ahora ya no será tan fácil que descubran tu racha de derrotas...*")
                return

            case "-stats":

                stats = self.bot.rps_stats.get(str(ctx.author.id), None)
                mensaje = None

                if stats is None:

                    mensaje = (f"A ver, {ctx.author.mention}, capo, máquina, " +
                               "no tenés stats porque nunca jugaste.")

                else:

                    victorias, derrotas, empates = stats

                    mensaje = (f"{ctx.author.mention}, tus estadísticas son: " +
                              f"`{victorias}` Victorias, `{derrotas}` Derrotas y " +
                              f"`{empates}` Empates.")

                await ctx.channel.send(content=mensaje, reference=ctx.message.to_reference())
                return

            case None:

                await ctx.channel.send(content=f"{CogRPS.elegir_frases(RPS_PHRASES)}\n\n" +
                                       "**¡Elige!** ¿Piedra, Papel o Tijeras?\n",
                                       reference=ctx.message.to_reference(),
                                       view=JuegoPPT(stats=self.bot.rps_stats))
                return

        if eleccion.upper() not in opciones:

            await ctx.channel.send(f"**[ERROR]** Capo, tenés que elegir entre `{piedra}`, " +
                                   f"`{papel}` o `{tijeras}`.",
                                   reference=ctx.message.to_reference())
            return

        await jugar_partida_ppt(eleccion, str(ctx.author.id), ctx.message, self.bot.rps_stats)
