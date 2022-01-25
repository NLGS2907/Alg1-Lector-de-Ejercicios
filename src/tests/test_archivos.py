"""
Módulo para tests del módulo 'archivos'.
"""

import unittest

from main.archivos.archivos import *


class TestArchivos(unittest.TestCase):
    """
    Tests de Archivos.
    """

    def test_1_valida_version(self) -> None:
        """
        Valida si hay versiones con nombres correctos.
        """

        self.assertTrue(version_es_valida("2c2019"))
        self.assertFalse(version_es_valida("3ex2801"))


if __name__ == "__main__":

    unittest.main()
