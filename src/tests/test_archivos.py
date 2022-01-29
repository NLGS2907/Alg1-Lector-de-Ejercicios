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

        arch_temp = "src/tests/json_simple.json"
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


if __name__ == "__main__":

    unittest.main()
