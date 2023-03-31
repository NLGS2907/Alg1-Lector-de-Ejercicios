"""
Tipos de datos de SQLite.
"""

from enum import Enum


class TiposDB(Enum):
    """
    Tipos de datos de una base de datos de SQLite.
    """

    NULL = "NULL" # No soportado en tablas estrictas

    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"

    # No soportado en tablas no estrictas
    INT = "INT" # Tiene diferencias sutiles con INTEGER
    ANY = "ANY"