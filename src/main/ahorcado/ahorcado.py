"""
Pequeño módulo que implementa la lógica de una partida de ahorcado.
"""

from typing import Optional
from random import choice

from ..archivos.archivos import cargar_lineas
from ..constantes.constantes import WORDS_PATH

class LetraAhorcado:
    """
    Pequeña clase para representar la letra de una frase
    en el ahorcado.
    """

    def __init__(self, valor: str, oculta: bool) -> None:
        """
        Inicializa una instancia de tipo 'LetraAhorcado'.
        """

        self.valor = valor
        self._oculta = oculta

    def __str__(self):
        """
        Muestra la letra con su valor y si está oculta o no.
        Está pensado para fines de Debug.
        """

        return f"Valor: {self.valor} | Oculta: {self._oculta}"

    @property
    def oculta(self) -> bool:
        """
        Propiedad que funciona como wrapper para 'self._oculto'.
        """

        return self._oculta

    @oculta.setter
    def oculta(self, nuevo_valor: bool) -> None:
        """
        La letra, una vez descubierta, no debe poderse volver a cubrir.
        """

        if not nuevo_valor:

            self._oculta = nuevo_valor

class Ahorcado:
    """
    Clase implementada para hacer un juego de ahorcado.
    """

    def __init__(self, frase: Optional[str]=None, **opciones) -> None:
        """
        Inicializa una instancia de tipo 'Ahorcado'.
        """

        frase_magica = (frase if frase else choice(cargar_lineas(WORDS_PATH)))
        self.maximos_intentos = opciones.get("vidas_maximas", 7)
        self.intentos = self.maximos_intentos

        self.display_id = 0  # Es inicializado después con el primer mensaje

        self.caracteres_usados = list()

        self.frase = list()

        for char in frase_magica:

            self.frase.append(LetraAhorcado(char, (False if char == ' ' else True)))

    def __str__(self) -> str:
        """
        Dibuja el ahorcado en ASCII art para que puedo ser impreso.
        """

        frase = "  ".join([(letra.valor if not letra.oculta else '_') for letra in self.frase])

        caracteres_usados = (" - ".join(self.caracteres_usados) if self.caracteres_usados else '-')

        piezas = list()

        simbolos = ('O', '|', '/', '\\', '|', '/', '\\')

        for i in range(6, -1, -1):

            piezas.append(simbolos[7 - (i + 1)] if self.intentos < (i + 1) else '')

        torso = (f"{piezas[2]} {piezas[1]} {piezas[3]}" if not piezas[2] and not piezas[3] else f"{piezas[2]}{piezas[1]}{piezas[3]}")

        estado = f"""```
    
    -=-= AHORCADO =-=-

    +--------+
    |        |
    |        {piezas[0]}
    |       {torso}            {frase}
    |        {piezas[4]}
    |       {piezas[5]} {piezas[6]}
    |                       LETRAS USADAS: {caracteres_usados}
    |
==============           -= VIDAS RESTANTES: {self.intentos} =-
```"""
        return estado

    def definir_display(self, display_id: int) -> None:
        """
        Define el ID del primer mensaje que es la pantalla del juego de ahorcado.
        """

        self.display_id = display_id

    def termino_juego(self) -> tuple[bool, bool]:
        """
        Determina si la partida ha terminado, y si fue una victoria o derrota.
        """

        if self.intentos <= 0:

            return True, False

        for letra in self.frase:

            if letra.oculta:

                return False, False

        return True, True
