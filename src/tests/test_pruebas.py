"""
Módulo para tests de prueba.
"""

import unittest


class TestPruebas(unittest.TestCase):
    """
    Tests de Pruebas.
    """

    def test_1_producto_simple(self) -> None:
        """
        Valida si hay versiones con nombres correctos.
        """

        self.assertEquals(2 * 3, 6)
        self.assertNotEquals(3 * 8, 56)


if __name__ == "__main__":

    unittest.main()