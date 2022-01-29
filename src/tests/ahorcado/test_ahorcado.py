"""
Módulo para tests de la clase 'Ahorcado'.
"""

import unittest
from os import remove as arch_remove

from src.main.ahorcado.ahorcado import *


class TestAhorcado(unittest.TestCase):
    """
    Tests de Ahorcado.
    """


    def test_1_carga_palabras_bien(self) -> None:
        """
        Carga una colección de palabras de prueba.
        """

        arch_temp = "src/tests/ahorcado/json_simple.json"

        with open(arch_temp, mode='w', encoding="utf-8") as arch:

            arch.write("bambú\nmanaza\npomelo")

        try:

            lista_palabras = Ahorcado.cargar_palabras(arch_temp)
            self.assertEqual(lista_palabras, ["bambú", "manaza", "pomelo"])


        finally:

            arch_remove(arch_temp)


    def test_2_cambia_frase_a_mayusculas(self) -> None:
        """
        La frase se cambia a una de todas mayúsculas.
        """

        frase = "Hola soy pablo"
        partida = Ahorcado(frase)

        self.assertEqual(frase.upper(), partida.get_frase())


    def test_3_adivina_una_letra(self) -> None:
        """
        Se adivina una letra correctamente.
        """

        partida = Ahorcado("MANZANA")

        fue_usada, esta_presente = partida.adivinar("a")

        self.assertFalse(fue_usada)
        self.assertTrue(esta_presente)


    def test_4_adivina_una_letra_repetida(self) -> None:
        """
        Se intenta adivinar una letra que ya fue usada.
        """

        partida = Ahorcado("NARANJA")
        partida.adivinar("a")

        fue_usada, esta_presente = partida.adivinar("a")

        self.assertTrue(fue_usada)
        self.assertTrue(esta_presente)


    def test_5_falla_en_adivinar_una_letra(self) -> None:
        """
        Se intenta adivinar una letra que no está en la frase.
        """

        partida = Ahorcado("BANANA")
        partida.adivinar("a")

        fue_usada, esta_presente = partida.adivinar("c")

        self.assertFalse(fue_usada)
        self.assertFalse(esta_presente)


    def test_5_falla_en_adivinar_una_letra_repetida(self) -> None:
        """
        Se intenta adivinar una letra que no está en la frase y que,
        además, ya había sido utilizada.
        """

        partida = Ahorcado("MARACUYA")
        partida.adivinar("t")

        fue_usada, esta_presente = partida.adivinar("t")

        self.assertTrue(fue_usada)
        self.assertFalse(esta_presente)


    def test_6_no_deja_adivinar_con_algo_que_no_sea_un_solo_caracter(self) -> None:
        """
        No debería de poder adivinarse con una cadena de más de un caracter.
        """

        partida = Ahorcado("SALTO")

        with self.assertRaises(ValueError):

            partida.adivinar("cambio")
