"""
Módulo para tests del módulo 'archivos'.
"""

import unittest
from os import remove as arch_remove

from src.main.archivos.archivos import *


class TestArchivos(unittest.TestCase):
    """
    Tests de Archivos.
    """

    def test_1_guarda_y_carga_json_simple(self) -> None:
        """
        Guarda y carga un archivo JSON simple
        """

        arch_temp = "src/tests/archivos/json_simple.json"
        dic_simple = {'a': 1, 'b': 2, 'c': 3, 'd': [4, 5]}

        guardar_json(dic_simple, arch_temp, sangria=None)

        try:

            with open(arch_temp) as arch:

                dic_simple_str = arch.read()

            dic_cargado = cargar_json(arch_temp)

            self.assertEqual(dic_simple_str, '{"a": 1, "b": 2, "c": 3, "d": [4, 5]}') # Si se guardó bien
            self.assertEqual(dic_cargado, dic_simple) # Si se cargó bien
            with self.assertRaises(FileNotFoundError):
                cargar_json("__path_basura__")

        finally:

            arch_remove(arch_temp)


    def test_2_valida_version(self) -> None:
        """
        Valida si hay versiones con nombres correctos.
        """

        self.assertTrue(version_es_valida("2c2019"))
        self.assertFalse(version_es_valida("3ex2801"))


    def test_3_valida_estructura_guia(self) -> None:
        """
        Debería haber exactamente 17 archivos JSON.
        """

        lista_archivos = archivos_guia("2c2019", "guia")
        lista_esperada = ["guia_1.json",
                          "guia_10.json",
                          "guia_11.json",
                          "guia_12.json",
                          "guia_13.json",
                          "guia_14.json",
                          "guia_15.json",
                          "guia_16.json",
                          "guia_17.json",
                          "guia_2.json",
                          "guia_3.json",
                          "guia_4.json",
                          "guia_5.json",
                          "guia_6.json",
                          "guia_7.json",
                          "guia_8.json",
                          "guia_9.json"]

        self.assertEqual(lista_archivos, lista_esperada)
        self.assertEqual(archivos_guia("2x2019", "guia"), None)
        with self.assertRaises(FileNotFoundError):

            archivos_guia("2c2019", "guiasa")


    def test_4_carga_una_guia_correctamente(self) -> None:
        """
        Carga un ejercicio y verifica que esté correcto.
        """

        guia_cargada = cargar_guia("2c2019", "guia")
        enunciado_esperado = {"titulo": [],
                            "descripcion": [
                            "Escribir una función que reciba dos números y devuelva su producto."
                            ],
                            "campos": {},
                            "pie": []}

        with self.assertRaises(FileNotFoundError):

            cargar_guia("2c2019", "guiasa")

        self.assertEqual(cargar_guia("2x2019", "guia"), None)
        self.assertEqual(guia_cargada["1"]["1"], enunciado_esperado)


    def test_5_cuenta_las_unidades_de_una_guia(self) -> None:
        """
        Deberían ser 17 unidades.
        """

        lista_cargada = lista_unidades(cargar_guia("2c2019", "guia"))
        lista_esperada = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
                          "14", "15", "16", "17"]

        self.assertEqual(lista_cargada, lista_esperada)
        self.assertNotEqual(lista_unidades({"version": "Ninguna, lol", "10": "judías", "40": 41, "337": "banana"}),
                            lista_esperada)
        with self.assertRaises(KeyError):

            lista_unidades({"10": "judías", "40": 41, "337": "banana"})


    def test_6_cuenta_los_ejercicios_de_una_unidad(self) -> None:
        """
        Cuenta los ejercicios de la unidad 15. Deberían de ser 13.
        """

        guia_cargada = cargar_guia("2c2019", "guia")
        lista_cargada = lista_ejercicios(guia_cargada, "15")
        lista_esperada = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]

        self.assertEqual(lista_cargada, lista_esperada)
        with self.assertRaises(KeyError):

            lista_ejercicios(guia_cargada, "18")            


if __name__ == "__main__":

    unittest.main()
