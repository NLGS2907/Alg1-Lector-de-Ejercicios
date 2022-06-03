"""
Cog para comandos de Piedra, Papel o Tijeras.
"""

from random import choices
from typing import TYPE_CHECKING, Optional

from discord import Interaction
from discord.app_commands import Choice
from discord.app_commands import choices as ds_choices
from discord.app_commands import command as appcommand
from discord.app_commands import describe

from ..archivos import cargar_json, guardar_json
from ..constantes import PROPERTIES_PATH, RPS_PHRASES
from ..interfaces import JuegoPPT
from ..ppt import jugar_partida_ppt
from .general import CogGeneral

if TYPE_CHECKING:

    from ..lector import Lector


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


    @appcommand(name="rps",
                description="Hace un pequeño juego de piedra-papel-tijeras.")
    @describe(eleccion="Elección de papel, piedra o tijeras.",
              opcion="La opción del comando.")
    @ds_choices(eleccion=[
                    Choice(name="Piedra", value="PIEDRA"),
                    Choice(name="Papel", value="PAPEL"),
                    Choice(name="Tijeras", value="TIJERAS")
                ],
                opcion=[
                    Choice(name="-reset", value="RESET"),
                    Choice(name="-stats", value="STATS")
                ])
    async def jugar_ppt(self,
                        interaction: Interaction,
                        eleccion: Optional[Choice[str]]=None,
                        opcion: Optional[Choice[str]]=None) -> None:
        """
        Simula un pequeño juego de 'piedra, papel o tijeras'.
        """

        if eleccion is not None:
            await interaction.response.send_message(content="¡Iniciando Partida!",
                                                    ephemeral=True)

            await jugar_partida_ppt(eleccion.value,
                                    str(interaction.user.id),
                                    self.bot.rps_stats,
                                    interaction)
            return

        opcion_a_usar = (opcion.value if opcion is not None else None)

        match opcion_a_usar:

            case "RESET":

                self.bot.rps_stats[str(interaction.user.id)] = [0, 0, 0]
                propiedades = cargar_json(PROPERTIES_PATH)
                propiedades["stats_ppt"] = self.bot.rps_stats
                guardar_json(propiedades, PROPERTIES_PATH)

                mensaje = (f"¡De acuerdo, {interaction.user.mention}! Ya reseté tus " +
                            "estadísticas a `0` - `0` - `0`.\n\n" +
                            "*Ahora ya no será tan fácil que descubran tu racha de derrotas...*")

                await interaction.response.send_message(content=mensaje,
                                                        ephemeral=True)
                return

            case "STATS":

                stats = self.bot.rps_stats.get(str(interaction.user.id), None)
                mensaje = None

                if stats is None:
                    mensaje = (f"A ver, {interaction.user.mention}, capo, máquina, " +
                               "no tenés stats porque nunca jugaste.")

                else:
                    victorias, derrotas, empates = stats
                    mensaje = (f"{interaction.user.mention}, tus estadísticas son: " +
                               f"`{victorias}` Victorias, `{derrotas}` Derrotas y " +
                               f"`{empates}` Empates.")

                await interaction.response.send_message(content=mensaje,
                                                        ephemeral=True)
                return

            case None:

                await interaction.response.send_message(content="¡Iniciando Partida!",
                                                        ephemeral=True)

                vista: JuegoPPT = JuegoPPT(stats=self.bot.rps_stats)
                mensaje_enviado = await interaction.channel.send(
                                        content=f"{CogRPS.elegir_frases(RPS_PHRASES)}\n\n" +
                                        "**¡Elige!** ¿Piedra, Papel o Tijeras?\n",
                                        view=vista)
                vista.msg = mensaje_enviado
                return


async def setup(bot: "Lector"):
    """
    Agrega el cog de este módulo al Lector.
    """

    await bot.add_cog(CogRPS(bot))
