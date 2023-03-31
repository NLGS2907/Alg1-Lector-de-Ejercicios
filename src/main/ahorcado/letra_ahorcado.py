"""
Módulo para contener la clase de una letra de ahorcado.
"""

class LetraAhorcado:
    """
    Pequeña clase para representar la letra de una frase
    en el ahorcado.
    """

    def __init__(self, valor: str, oculta: bool) -> None:
        """
        Inicializa una instancia de tipo 'LetraAhorcado'.
        """

        if not isinstance(valor, str):

            raise TypeError(f"'{valor}' es de tipo '{type(valor).__name__}'." +
                            "Debería ser de tipo 'str'")

        if not len(valor) == 1:

            raise ValueError(f"'{valor}' debe ser un string de un (1) solo caracter")

        if not isinstance(oculta, bool):

            raise TypeError(f"Valor de 'oculta' ({oculta}) debería ser 'True' or 'False'.")

        self.valor: str = valor
        self._oculta: bool = oculta

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
