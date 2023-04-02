"""
Módulo de bases de datos.
"""

from os import PathLike
from sqlite3 import connect, OperationalError
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from .db_tipos import TiposDB

DictConds = Any
ValoresResolucion = Literal["ABORT", "FAIL", "IGNORE", "REPLACE", "ROLLBACK"]
_SingularResult = Tuple[Union[None, int, str]]
FetchResult = Union[List[_SingularResult], _SingularResult]
CursorDesc = Dict[str, Union[None, Tuple[str, ...], str, int]]
DictLlaveForanea = Dict[str, Tuple[str, str]]

DEFAULT_DB: PathLike = "src/main/db/db.sqlite3"
RESOLUCIONES: Tuple[str, ...] = "ABORT", "FAIL", "IGNORE", "REPLACE", "IGNORE"
ESTRICTO_NO_ACEPTADOS: list[TiposDB] = [TiposDB.NULL]
NO_ESTRICTO_NO_ACEPTADOS: list[TiposDB] = [TiposDB.INT, TiposDB.ANY]


def ejecutar_comando(comando: str, es_script: bool, db_path: PathLike[str]) -> CursorDesc:
    """
    Ejecuta un comando arbitrario, pasándolo tal cual a
    sqlite para parsear.
    """

    data = {}

    with connect(db_path) as con:
        cur = con.cursor()

        if es_script:
            cur.executescript(comando)
        else:
            cur.execute(comando)

        # Juntando datos
        data["description"] = (tuple(d[0] for d in cur.description)
                               if cur.description is not None
                               else None)
        data["lastrowid"] = cur.lastrowid
        data["rowcount"] = cur.rowcount

    return data


def ejecutar_linea(comando: str, db_path: PathLike[str]="") -> CursorDesc:
    """
    Ejecuta un comando de SQL que no requiera sacar datos.
    """

    return ejecutar_comando(comando, False, db_path or DEFAULT_DB)


def ejecutar_script(comando: str, db_path: PathLike[str]="") -> CursorDesc:
    """
    Ejecuta un comando de SQL de varias líneas.
    """

    return ejecutar_comando(comando, True, db_path or DEFAULT_DB)


def _condiciones_where(**condiciones: DictConds) -> str:
    "Crea una expresión SQL con todas las condiciones en el kwargs."

    extra = None

    try:
        extra = condiciones.pop("where")
        if not isinstance(extra, tuple):
            raise TypeError("condiciones extra del parametro 'where' " +
                            "deben ser una tupla de strings.")
    except KeyError:
        extra = tuple()

    conds = " AND ".join([f"{k}={v!r}" for k, v in condiciones.items()] + list(extra))
    return ('' if not conds else f" WHERE {conds}")


def _protocolo_resolucion(resolucion: Optional[ValoresResolucion]=None) -> str:
    "Parsea una opcion para definir un protocolo en caso de que una operacion falle."

    if resolucion is None:
        res_protocol = ''
    elif resolucion.upper() not in RESOLUCIONES:
        raise ValueError(f"Tipo de resolucion debe ser uno de {RESOLUCIONES}")
    else:
        res_protocol = f" OR {resolucion} "

    return res_protocol


def nombres_tablas(db_path: PathLike=DEFAULT_DB) -> tuple[str, ...]:
    """
    Devuelve una tupla con todos los nombres de las tablas que tiene la DB.
    """

    with connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = cur.fetchall()

    return tuple(t[0] for t in res)


def existe_tabla(nombre_tabla: str, db_path: PathLike=DEFAULT_DB)-> bool:
    """
    Verifica, por su nombre, si una tabla existe en la DB especificada.
    """

    return nombre_tabla in nombres_tablas(db_path=db_path)


def nombres_columnas(tabla: str, db_path: PathLike=DEFAULT_DB) -> tuple[str, ...]:
    """
    Devuelve los nombres de las columnas de una tabla.
    """

    with connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM :tabla", {"tabla": tabla})
        nombres = tuple(desc[0] for desc in cur.description)

    return nombres


def _formatear_llaves_foraneas(dic_llaves: DictLlaveForanea,
                               nombres_revisados: list[str]) -> str:
    """
    Formatea las llaves foráneas en un formato amigable.
    """

    llaves = []

    for nombre_col, (tabla_for, col_for) in dic_llaves.items():
        if nombre_col not in nombres_revisados:
            raise ValueError((f"Nombre de llave foránea {nombre_col!r} no coincide " +
                              "con los de la tabla"))

        llaves.append(f"FOREIGN KEY({nombre_col}) REFERENCES {tabla_for}({col_for})")

    return ", ".join(llaves)


def crear_tabla(nombre: str,
                *,
                db_path: PathLike=DEFAULT_DB,
                estricta: bool=True,
                llave_primaria: Optional[str]=None,
                llaves_foraneas: Optional[DictLlaveForanea]=None,
                **kwargs: TiposDB) -> Optional[CursorDesc]:
    """
    Intenta crear una nueva tabla, con las especificaciones dadas.

    Si no tiene éxito, devuelve `None`.
    """

    if nombre in nombres_tablas(db_path):
        return None

    tipos = []
    _nombres_revisados = []

    for nombre_col, tipo_col in kwargs.items():
        nom_col = nombre_col.lower()

        if not isinstance(tipo_col, TiposDB):
            raise TypeError(f"El tipo de columna debe ser {TiposDB.__name__}")
        
        if nom_col in _nombres_revisados:
            raise ValueError(f"Nombre de columna {nom_col!r} repetido")

        if estricta and tipo_col in ESTRICTO_NO_ACEPTADOS:
            raise ValueError(f"Tipo de dato {tipo_col.value} no válido en tabla estricta")

        if not estricta and tipo_col in NO_ESTRICTO_NO_ACEPTADOS:
            raise ValueError(f"Tipo de dato {tipo_col.value} no válido en tabla no estricta")

        es_llave = (" PRIMARY KEY"
                     if (llave_primaria is not None
                         and llave_primaria.lower() == nom_col)
                     else "")
        tipos.append(f"{nom_col} {tipo_col.value}{es_llave}")
        _nombres_revisados.append(nom_col)

    cols = ", ".join(tipos)
    es_estricta = (" STRICT" if estricta else "")
    foranea = (""
               if llaves_foraneas is None
               else f", {_formatear_llaves_foraneas(llaves_foraneas, _nombres_revisados)}")

    return ejecutar_linea(comando=f"CREATE TABLE {nombre} ({cols}{foranea}){es_estricta};",
                          db_path=db_path)


def sacar_datos_de_tabla(tabla: str,
                         sacar_uno: bool=False,
                         ignorar_excepciones: bool=False,
                         **condiciones: DictConds) -> FetchResult:
    "Saca datos de una base de datos."

    res = None
    conds = _condiciones_where(**condiciones)

    try:
        with connect(DEFAULT_DB) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {tabla}{conds};")
            res = (cur.fetchone() if sacar_uno else cur.fetchall())
    except OperationalError as err:
        if ignorar_excepciones:
            return res

        raise err from err

    return res


def borrar_datos_de_tabla(tabla: str,
                          **condiciones: DictConds) -> int:
    """
    Borra datos de una base de datos.
    Devuelve la cantidad de filas afectadas.

    * NO oncluye una opción LIMIT.
    """

    conds = _condiciones_where(**condiciones)
    cuenta = 0

    with connect(DEFAULT_DB) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM {tabla}{conds};")
        cuenta += cur.rowcount

    return cuenta


def insertar_datos_en_tabla(tabla: str,
                            resolucion: Optional[ValoresResolucion]=None,
                            *,
                            llave_primaria_por_defecto: bool=True,
                            valores=Tuple[Any, ...]) -> int:
    """
    Intenta insertar datos en una tabla.
    Devuelve la cantidad de filas afectadas.
    """

    protocolo_res = _protocolo_resolucion(resolucion)
    valores_wrapped = [f"{v!r}" for v in valores]
    valores_finales = f"({'?, ' if llave_primaria_por_defecto else ''}{', '.join(valores_wrapped)})"
    cuenta = 0

    with connect(DEFAULT_DB) as con:
        cur = con.cursor()
        cur.executescript(f"INSERT{protocolo_res} INTO {tabla} VALUES{valores_finales};")
        cuenta += cur.rowcount

    return cuenta


def actualizar_dato_de_tabla(tabla: str,
                              resolucion: Optional[ValoresResolucion]=None,
                              *,
                              nombre_col: str,
                              valor: Any,
                              **condiciones: DictConds) -> int:
    """
    Actualiza un dato ya presente en tablas.
    Devuelve la cantidad de filas afectadas.
    """

    if not isinstance(nombre_col, str):
        raise TypeError("El nombre de la columna debe ser de tipo string.")

    conds = _condiciones_where(**condiciones)
    res_protocol = _protocolo_resolucion(resolucion)
    cuenta = 0

    with connect(DEFAULT_DB) as con:
        cur = con.cursor()
        cur.execute(f"UPDATE{res_protocol} {tabla} SET {nombre_col}={valor!r} {conds};")
        cuenta += cur.rowcount

    return cuenta


def existe_dato_en_tabla(tabla: str,
                         **condiciones: DictConds) -> bool:
    "Se fija si existe un dato coincidente en la tabla especificada."

    return bool(sacar_datos_de_tabla(tabla, **condiciones))


def emoji_str(codepoint: str) -> str:
    """
    Función auxiliar que convierte un string del formato 'U+XXXX' a '\\U0000XXXX'.
    """

    if not codepoint.startswith("U+"):
        raise ValueError("El string debe tener el formato 'U+XXXX'.")

    escape = chr(int(codepoint[2:], 16)).encode("unicode-escape").decode("UTF-8") # '\\uXXXX'
    return eval(f"\"{escape}\"") # Evaluarlo porque sino agarra el string tal cual
