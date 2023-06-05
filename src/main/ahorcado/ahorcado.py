"""
Pequeño módulo que implementa la lógica de una partida de ahorcado.
"""

from random import choice
from typing import Optional, TypeAlias

from ..db.atajos import get_ruta_palabras
from .letra_ahorcado import LetraAhorcado

ListaLetras: TypeAlias = list[LetraAhorcado]


class Ahorcado:
    """
    Clase implementada para hacer un juego de ahorcado.
    """

    @staticmethod
    def cargar_palabras(nombre_archivo: str) -> list[str]:
        """
        Devuelve una lista de las lineas de un archivo que tiene solo
        un valor en cada una.
        """

        lineas = []

        with open(nombre_archivo, encoding="utf-8") as archivo:

            lineas = [linea.rstrip() for linea in archivo]

        return lineas


    def __init__(self,
                 *,
                 frase: Optional[str]=None,
                 vidas_maximas: int=7,
                 id_mensaje_padre: int = int) -> None:
        """
        Inicializa una instancia de tipo 'Ahorcado'.
        """

        frase_magica: str = (frase if frase else choice(Ahorcado.cargar_palabras(get_ruta_palabras())))
        self.maximos_intentos: int = vidas_maximas
        self.intentos: int = self.maximos_intentos
        self.id_mensaje_padre: int = id_mensaje_padre

        self.caracteres_usados: ListaLetras = []
        self.frase: ListaLetras = []

        for char in frase_magica:

            self.frase.append(LetraAhorcado(char.upper(), (not char == ' ')))


    def __str__(self) -> str:
        """
        Dibuja el ahorcado en ASCII art para que puedo ser impreso.
        """

        frase = "  ".join([(letra.valor if not letra.oculta else '_') for letra in self.frase])

        caracteres_usados = (" - ".join(self.caracteres_usados) if self.caracteres_usados else '-')

        piezas = []

        simbolos = ('O', '|', '/', '\\', '|', '/', '\\')

        for i in range(6, -1, -1):

            piezas.append(simbolos[7 - (i + 1)] if self.intentos < (i + 1) else '')

        torso = (f"{piezas[2]} {piezas[1]} {piezas[3]}"
                 if (not piezas[2] and not piezas[3])
                 else (f"{piezas[2]}{piezas[1]}{piezas[3]}"))

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


    def get_frase(self) -> str:
        """
        Devuelve una cadena de la frase.
        """

        return ''.join([char.valor for char in self.frase])


    def adivinar(self, char: str) -> tuple[bool, bool]:
        """
        Intenta adivinar una letra de ahorcado.
        Devuelve una tupla de dos valores booleanos, siendo el primero si
        la letra está en los caracteres usados, y el segundo si está en
        la frase.
        """

        if not len(char) == 1:

            raise ValueError(f"'{char}' debe ser una cadena de un (1) solo caracter")

        char = char.upper()
        fue_usado = char in self.caracteres_usados
        esta_presente = None

        if not fue_usado:

            self.caracteres_usados.append(char)

        if char in [l.valor for l in self.frase]:

            for letrita in self.frase:

                if letrita.valor == char:

                    letrita.oculta = False

            esta_presente = True

        else:

            self.intentos -= 1
            esta_presente = False

        return fue_usado, esta_presente


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
