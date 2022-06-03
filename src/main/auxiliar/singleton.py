"""
Módulo que contiene la metaclase para objetos con patrón singleton.
"""

class Singleton(type):
    """
    Metaclase 'Singleton'.
    """

    _instancias = {}

    def __call__(cls, *args, **kwargs):
        """
        Llama a este objeto como si fuera una función.
        """

        if cls not in cls._instancias:

            cls._instancias[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instancias[cls]
