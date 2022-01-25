"""
Enumeración de estado del resultado de una partida de PPT.
"""

from enum import Enum


class Condicion(Enum):
    """
    Posibles estados del resultado de la partida.
    """

    VICTORIA = 0

    DERROTA = 1

    EMPATE = 2
