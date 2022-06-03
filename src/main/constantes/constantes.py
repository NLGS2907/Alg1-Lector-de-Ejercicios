"""
Módulo para almacenar constantes, y para evitar import loops.
"""

from os import getenv

from dotenv import load_dotenv

load_dotenv()


TOKEN = getenv("DISCORD_TOKEN")

BOT_ID = 889312376036425810
"""
El ID específico de este bot.
"""

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

BOT_VERSION = "1.3.0"
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

PROPERTIES_PATH = "src/main/json/propiedades.json"

GUIA_PATH = "guia"
"""
Dirección (relativa al directorio raíz) de la carpeta de guías.
"""

LOG_PATH = "lector.log"
"""
El path donde se encuentra el registro.
"""

WORDS_PATH = "src/main/txt/palabras.txt"

COGS_PATH = "src/main/cogs"

WHATSNEW_MESSAGE = "src/main/json/whatsnew_msg.json"

DATE_FORMAT = "%Y-%m-%d_%H-%M-%S_%f"

REPO_URL = "https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios"
"""
La URL del repositorio donde está el código fuente del bot.
"""

USER_CONSULT = "**{mencion}** ha consultado:"

TITLE_FORMAT = "**Unidad** {unidad} - \"{titulo}\"  |  **Ejercicio** {ejercicio}"

EXT = ".json"
"""
La extensión de archivo usada para almacenar el texto que son los ejercicios
de la guía.
"""

RPS_PHRASES = ["Conque sí, ¿Eh? Veo que estás listo para otra derrota...",
"¿Es tu primera vez contra mí? Tranquilo, iré fácil...\n\n\n*...nah.*",
"De por sí es impresionante que hayas encontrado este comando, ¿Te lo dijo alguien o tenés " +
"la costumbre de husmear en el código fuente?",
"Pepito claló... Pepito clavó un clalit... Pablito clavó un calvito... " +
"¡Agh, nunca me sale! ¡Da igual!",
"Voy a ver si te gano con los ojos cerrados.",
"A jugar, pibe.",
"Y pensar que yo era un lector de ejercicios nomás...\n\nMeh, un easter egg o dos no están mal.",
"¿Quién viene a perder? Vos. Sí, vos.",
"Si sigues intentando puede que encuentres otro secreto... " +
"si no los husmeas en el código fuente, claro.",
"¿Te gusta mi logo? Lo hizo mi creador (pintando una imagen de por ahí de google el vago), " +
"pero me gusta.",
# Si estás mirando esto es porque eres un husmeador aguafiestas, ¡Consigue el secreto por tí mismo!
# O puede que seas un dev respetable que viene a ver el código, huh. En ese caso, bienvenido...
"He perdido la cuenta de cuántas veces he sido corrido para probarme. ¿Sabías que superan las " +
"100 veces? En fin...",
"Si alguien te dice que no estoy hecho en python, es que miente.",
"|| Míralo al clickea-spoilers, ¡Estarás contento! ||",
"Yo solía estar hosteado en ***Heroku***, hasta que mantenerme dejó de ser gratis. " +
"Ahora corro en un servidor por SSH.",
"""```python
def aprobar_materia(nota: int) -> bool:

    if nota < 4:

        print("Para la próxima crack")
        return False

    return True
```
Yo también sé codear, ejem.""",
"0101010001101000011001010111001101100101001000000110000101110010011001010010000001101110011011" +
"1101110100001000000111010001101000011001010010000001100001011011100110010001110010011011110110" +
"1001011001000111001100100000011110010110111101110101001000000110000101110010011001010010000001" +
"1011000110111101101111011010110110100101101110011001110010000001100110011011110111001000101110" +
"0010111000101110",
"**¡¡¡Has encontrado el secreto!!!** Toma: https://i.imgur.com/eFo6haC.png \n\n\n" +
"*Ahora en serio, juguemos.*"
]
