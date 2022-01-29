"""
Módulo para tests de la clase 'LetraAhorcado'.
"""

import unittest

from src.main.ahorcado.letra_ahorcado import *


class TestLetraAhorcado(unittest.TestCase):
    """
    Tests de letras de Ahorcado.
    """

    def test_1_se_crea_correctamente(self) -> None:
        """
        Debe de ser una cadena de 1 solo caracter.
        """

        with self.assertRaises(TypeError):

            LetraAhorcado(25, True)

        with self.assertRaises(ValueError):

            LetraAhorcado("manzana", True)

        with self.assertRaises(TypeError):

            LetraAhorcado("n", 56)


    def test_2_se_representa_bien(self) -> None:
        """
        ``str(LetraAhorcado)`` debe tener el formato adecuado.
        """

        letra = LetraAhorcado('a', False)
        cadena_esperada = "Valor: a | Oculta: False"

        self.assertEqual(str(letra), cadena_esperada)


    def test_3_una_vez_descubierta_no_se_puede_ocultar(self) -> None:
        """
        Una vez descubierta, la letra no puede volverse a ocultar. 
        """

        letra = LetraAhorcado('b', True)
        otra_letra = LetraAhorcado('b', False)

        self.assertEqual(letra.oculta, True)
        self.assertEqual(otra_letra.oculta, False)

        letra.oculta = False
        otra_letra.oculta = True

        self.assertEqual(letra.oculta, False)
        self.assertEqual(otra_letra.oculta, False)