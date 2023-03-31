"""
Modal para adivinar una letra de ahorcado.
"""

from typing import TYPE_CHECKING

from discord import Interaction
from discord.enums import TextStyle
from discord.ui import Modal, TextInput

if TYPE_CHECKING:
    from .guess_btn import VistaAdivinacion
    from ...ahorcado import Ahorcado


class ModalAdivinacion(Modal):
    """
    Modal que adivina la letra.
    """

    letra: TextInput = TextInput(label="Adivina una letra.",
                                 style=TextStyle.short,
                                 custom_id="hanged_guess_modal_input",
                                 placeholder="Ingresa sólo un caracter.",
                                 required=True,
                                 min_length=1,
                                 max_length=1,
                                 row=0)


    def __init__(self, vista: "VistaAdivinacion") -> None:
        """
        Inicializa una instancia de 'CommandDB'.
        """

        super().__init__(timeout=None,
                         title="Letra de Ahorcado",
                         custom_id="hanged_guess_modal")

        self.vista: "VistaAdivinacion" = vista


    async def on_error(self, interaccion: Interaction, error: Exception) -> None:
        """
        Un error ocurrió.
        """

        msg = f"**[ERROR]** {str(error)}"
        await interaccion.response.send_message(content=msg,
                                                ephemeral=True)


    async def on_submit(self, interaccion: Interaction) -> None:
        """
        Procesa la letra.
        """

        await self.hanged_guess(interaccion, self.letra.value)

        termino, es_victoria = self.vista.bot.partidas[str(interaccion.channel.id)].termino_juego()

        if termino:
            await self.fin_del_juego(interaccion, es_victoria)


    async def hanged_guess(self, interaccion: Interaction, char: str) -> None:
        """
        Intenta adivinar una letra u otro caracter, si no fue usado ya.
        """

        if not char:
            await interaccion.response.send_message(content=f"**[ERROR]** `{char}` no es " +
                                                            "una letra válida.",
                                                    ephemeral=True)
            return

        partida = self.vista.bot.encontrar_partida(str(interaccion.channel.id))

        # 'letra' debe ser, efectivamente, una cadena de un solo caracter
        if any((not partida, partida.intentos <= 0, not len(char) == 1)):
            await interaccion.response.send_message(content=f"**[ERROR]** `{char}` debe ser " +
                                                            "una cadena de un sólo caracter.",
                                                    ephemeral=True)
            return

        fue_usado, esta_presente = partida.adivinar(char)
        char = char.upper()

        if fue_usado:
            await interaccion.response.send_message(f"¡Mal ahí, {interaccion.user.mention}! " +
                                                    f"¡El caracter `{char}` ya fue utilizado! " +
                                                    "Probá con otra cosa...")
            return

        if esta_presente:
            await interaccion.response.send_message(f"¡{interaccion.user.mention} ha acertado " +
                                                    f"el caracter `{char}`!")

        else:
            s = ("s" if partida.intentos > 1 else "")
            await interaccion.response.send_message(f"¡Ole! ¡{interaccion.user.mention} ha " +
                                                    f"dicho el caracter `{char}`, " +
                                                    "que no se encuentra en la palabra! " +
                                                    f"Quedan {partida.intentos} intento{s}...")

        await interaccion.message.edit(content=str(partida),
                                       view=self.vista)


    async def fin_del_juego(self, interaccion: Interaction, es_victoria: bool) -> None:
        """
        Hace las acciones correspondientes una vez que termina el juego.
        """

        partida_terminada: "Ahorcado" = self.vista.bot.partidas.pop(str(interaccion.channel.id))
        frase_magica = ''.join([c.valor for c in partida_terminada.frase])
        ultimo_caracter = partida_terminada.caracteres_usados.pop()
        es_una_vida = (partida_terminada.intentos == 1)

        if es_victoria:
            contenido = (f"Resultado de partida `{interaccion.channel.name}`: " +
            f"**[VICTORIA]**\n\n¡{interaccion.user.mention} se hizo con la victoria con la letra " +
            f"`{ultimo_caracter}`, y con `{partida_terminada.intentos}` " +
            f"vida{'' if es_una_vida else 's'} de sobra! En efecto, la frase era `{frase_magica}`.")

        else:
            contenido = (f"Resultado de partida `{interaccion.channel.name}`: **[DERROTA]**" +
            f"\n\n¡Vergüenza para {interaccion.user.mention}! Ha fastidiado la partida " +
            f"diciendo el caracter `{ultimo_caracter}`. La frase era `{frase_magica}`.")

        await interaccion.channel.parent.send(content=contenido,
                                              delete_after=10.0)
        mensaje_original = await interaccion.channel.parent.fetch_message(partida_terminada.id_mensaje_padre)
        if mensaje_original:
            await mensaje_original.delete()
        await interaccion.channel.delete()
