"""
Módulo para almacenar constantes, y para evitar import loops.
"""

from random import choices

from dotenv import load_dotenv
load_dotenv()

from os import getenv


TOKEN = getenv("DISCORD_TOKEN")

CLIENT_CONFIG = {"client_id" : getenv("IMGUR_ID"),
                 "client_secret" : getenv("IMGUR_SECRET"),
                 "access_token": getenv("IMGUR_ACCESS_TOKEN"),
                 "expires_in": getenv("IMGUR_EXPIRES_IN"),
                 "token_type": "bearer",
                 "refresh_token": getenv("IMGUR_REFRESH_TOKEN"),
                 "account_username": "NLGS",
                 "account_id": 149426433
}
"""
Datos de acceso y registro del cliente.
"""

MEMES_ALBUM_NAME = "Memes de Python"
"""
El nombre del album a utilizar.
A poder ser, no modificar.
"""

ALGORITMOS_ESSAYA_ID = 653341065767550976
"""
Para más facilidad, se tiene a mano una constante
con el ID del servidor de Algoritmos I - Essaya.
"""

ROL_DIEGO_ID = 653341579389435927

ROL_DOCENTE_ID = 653341523886342145

BOT_VERSION = "1.1.0"
"""
La versión del bot a ser usada.

Esto es más bien una convención a ser usada para llevar control
sobre el desarrollo del bot.
"""

DEFAULT_PREFIX = '!'
"""
El prefijo por defecto que los servidores a los que se una el bot
tendrá inicialmente.
"""

DEFAULT_VERSION = "2c2019"
"""
La versión de la guía por defecto, si la especificada no se encontrase.
"""

# Las siguientes direcciones son relativas al directorio raíz, no de la carpeta 'src'

PREFIXES_PATH = "src/prefixes.csv"

VERSIONS_PATH = "src/versions.csv"

STATS_PATH = "src/rps_stats.csv"

GUIA_PATH = "guia"
"""
Dirección (relativa al directorio raíz) de la carpeta de guías.
"""

LOG_PATH = "lector.log"
"""
El path donde se encuentra el registro.
"""

DATE_FORMAT = "%Y-%m-%d_%H-%M-%S_%f"

REPO_URL = "https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios"
"""
La URL del repositorio donde está el código fuente del bot.
"""

MESSAGE_FORMAT = "**{mention}** ha consultado:\n\n>>> **Unidad** {unidad} - \"{titulo}\"  |  **Ejercicio** {ejercicio}:\n\n**{unidad}.{ejercicio}.** {enunciado}"

INFO_MESSAGE = {

'1' : """>>> **- Lector de Ejercicios (v{version_bot}) -\t(1 / 2)**

Versión de la guía para este servidor: `{version}`

`{prefix}info|i -dm` muestra esta lista.

`{prefix}ej|ejercicio|enunciado <unidad> <ejercicio> -dm` para mostrar el ejercicio de la unidad correspondiente de la guía.

`{prefix}random|aleatorio|r <unidad posible>, <sentido> -dm` para mostrar un ejercicio al azar. 'unidad_posible' es de
dónde empezar a buscar, y 'sentido' es el parámetro de búsqueda, y toma los valores '=', '<', '<=',
'>' o '>='.
Por ejemplo, `{prefix}random 12 <=` devuelve un ejercicio aleatorio de alguna guía anterior o igual a la guía 12.

`{prefix}prefix|prefijo <nuevo_prefijo>` cambia el prefijo de los comandos a 'nuevo_prefijo'.

`{prefix}guia|guia_version|gver <nueva_version>` cambia la versión de la guía que utilizar, si es una versión válida.

`{prefix}meme -add|-agregar|<numero>` para generar un meme aleatorio, o el de la posición `numero`, o con el parámetro `add` para intentar añadirlo a la colección. 
""",

'2' : """>>> **- Lector de Ejercicios (v{version_bot}) -\t(2 / 2)**

Versión de la guía para este servidor: `{version}`

`{prefix}hanged|ahorcado <vidas> <*frase>` para reservar una sala de ahorcado. Esta es en forma de un hilo temporal.
Si se hace una partida personalizada con `<*frase>` determinada por el usuario, se recomienda encerrarlo en '\|\|'.
Así, \|\|palabra\|\| se ve como ||palabra||. Esto sirve para desalentar ver la respuesta de primeras.

También, si se está dentro de una sala de ahorcado:

`{prefix}guess|adivinar <caracter>` para tratar de adivinar un solo caracter de la frase oculta.

`{prefix}display|mostrar` para mostrar de nuevo la pantalla del juego de ahorcado. Ahora esta nueva pantalla será la
que se actualice para mostrar el avance del juego.

`{prefix}clear|clean|cls <limite> | -full` para limpiar los mensajes del bot. `<limite>` es la cantidad de mensajes
que verificar (no los que serán borrados, aunque puede ser el caso). `full` elimina no sólo los mensajes del bot
si no también los de todos los usuarios que invocan sus comandos.

`{prefix}version|ver` para mostrar en un mensaje breve la versión actual del bot. 


*desarrollado por Franco 'NLGS' Lighterman Reismann.*
"""
}

EXT = ".txt"
"""
La extensión de archivo usada para almacenar el texto que son los ejercicios
de la guía.
"""

RPS_PHRASES = ["Conque sí, ¿Eh? Veo que estás listo para otra derrota...",
"¿Es tu primera vez contra mí? Tranquilo, iré fácil...\n\n\n...nah.",
"De por sí es impresionante que hayas encontrado este comando, ¿Te lo dijo alguien o tenés la costumbre de husmear en el código fuente?",
"Pepito claló... Pepito clavó un clalit... Pablito clavó un calvito... ¡Agh, nunca me sale! ¡Da igual!",
"Voy a ver si te gano con los ojos cerrados.",
"A jugar, pibe.",
"Y pensar que yo era un lector de ejercicios nomás...\n\nMeh, un easter egg o dos no están mal.",
"¿Quién viene a perder? Vos. Sí, vos.",
"Si sigues intentando puede que encuentres otro secreto... si no los husmeas en el código fuente, claro.",
"¿Te gusta mi logo? Lo hizo mi creador (pintando una imagen de por ahí de google el vago), pero me gusta.",
# Si estás mirando esto es porque eres un husmeador aguafiestas, ¡Consigue el secreto por tí mismo!
# O puede que seas un dev respetable que viene a ver el código, huh. En ese caso, bienvenido...
"He perdido la cuenta de cuántas veces he sido corrido para probarme. ¿Sabías que superan las 100 veces? En fin...",
"Si alguien te dice que no estoy hecho en python, es que miente.",
"|| Míralo al clickea-spoilers, ¡Estarás contento! ||",
"Yo solía estar hosteado en ***Heroku***, hasta que mantenerme dejó de ser gratis. Ahora corro en un servidor por SSH.",
"""```python
def aprobar_materia(nota: int) -> bool:
    
    if nota < 4:

        print("Para la próxima crack")
        return False

    return True
```
Yo también sé codear, ejem.""",
"**¡¡¡Has encontrado el secreto!!!** Toma: https://i.imgur.com/eFo6haC.png \n\n\nhora en serio, juguemos."
]

WHATSNEW = f""">>> **- Novedades de la versión `{BOT_VERSION}` -**

Esta versión introduce una nueva imagen para el bot, manejo de imágenes por
Imgur, para mejor experiencia de memes. También se introducen menús contextuales para `ej` y `guia`.

* **¡Nuevo Logo!** Las referencias se encuentran en la carpeta de *imágenes*.

* **Hace uso de `imgur-python`** para manejar imágenes a través del bot de Discord.

* **Nuevo Archivo `cliente_imgur.py`** para guardar la lógica de la
aplicación que representa el cliente de Imgur.

* **Ahora el comando `meme` ya no acepta ids de links.** Sin embargo, ahora
acepta que se le pase el índice de meme si se quiere uno en concreto de la
colección en Imgur.

* **Nuevo parámetro `add` para el comando `meme`**. Con esto, si el mensaje que envía el comando refiere a una imagen, se agrega esta a la colección de memes.

* **Nuevo Archivo `interfaces.py`** en donde guardar las interfaces usadas
en los mensajes del bot.

* **Ahora `guia` tiene un menú contextual.** Permite seleccionar más
intuitivamente las versiones de la guía, y se llama con `guia` sin
parámetros.

* **Similarmente con `ej`,** ahora este tiene no sólo también un menú
selector, si no también hace uso de botones para navegar por los ejercicios.

* **Agregado banco entero de palabras en español para el ahorcado.** Ahora
hay `80946` combinaciones posibles. Unas pocas más.

* **El bot ahora es más** ¿...competitivo?
"""


def elegir_frases(opciones: list[str]=RPS_PHRASES) -> str:
    """
    Elige con distinta probabilidad las opciones
    """

    num_opciones = len(opciones)

    pesos = ([10] * (num_opciones - 1) if num_opciones > 1 else []) + [1]

    return ''.join(choices(opciones, weights=pesos))