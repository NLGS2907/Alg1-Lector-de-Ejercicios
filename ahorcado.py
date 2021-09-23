from typing import Optional

class Ahorcado:
    """
    Clase implementada para hacer un juego de ahorcado.
    """

    def __init__(self, palabra: Optional[str]=None) -> None:
        """
        Crea una instancia de tipo 'Ahorcado'.
        """

        self.palabra_magica = palabra
        self.maximos_intentos = 6