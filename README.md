# Lector de Ejercicios

<img alt="exercise_reader.png" align="left" src="img/exercise_reader.png" height=128 width=128 />

<p align="left">

![status](https://dcbadge.vercel.app/api/shield/889312376036425810?bot=true?logoColor=presence&theme=discord)

![version](https://img.shields.io/badge/version-1.4.1-brightgreen)
![estrellas](https://img.shields.io/github/stars/NLGS2907/Alg1-Lector-de-Ejercicios?label=Estrellas&style=social)
![forks](https://img.shields.io/github/forks/NLGS2907/Alg1-Lector-de-Ejercicios?style=social)
![Tests](https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios/actions/workflows/tests.yml/badge.svg)
![Pylint](https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios/actions/workflows/pylint.yml/badge.svg)

Este bot de discord está pensado para usarse principalmente en el discord de la materia Algoritmos y Programación I,
de la Facultad de Ingeniería de la UBA, aunque puede utilizarse para cualquier servidor que lo quiera.
</p>

<hr/>

* [**Enlace de Invitación**](https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=294205467712&scope=bot%20applications.commands)

* **[Dependencias](requirements.txt)**

  | Nombre | Versión | Extra Info. |
  | :-: | :-: | :-: |
  | [discord.py](https://pypi.org/project/discord.py/) | 2.2.2 |  |
  | [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.0.0 |  |

* **[Licencia MIT](LICENSE)**

* **índice**
  - [Cómo Ejecutar](#cómo-ejecutar)
  - [Changelog](#changelog)

<hr/>

## Cómo Ejecutar

Pararse dentro de la carpeta [`run`](run), o de la carpeta raíz, y ejecutar uno de los dos
archivos presentes en [`run`](run), según el SO.

### **Ejemplos:**
```bat
@REM para Windows
cd run
./run.bat
```
```sh
# para Linux u otro entorno de shell
cd run
./run.sh
```

<hr/>

## Changelog:

|       Version     |
|     :---------:   |
|**[v1.4.1](#v141)**|
|  [v1.4.0](#v140)  |
|  [v1.3.0](#v130)  |
|  [v1.2.1](#v121)  |
|  [v1.2.0](#v120)  |
|  [v1.1.0](#v110)  |
|  [v1.0.4](#v104)  |
|  [v1.0.3](#v103)  |
|  [v1.0.2](#v102)  |
|  [v1.0.1](#v101)  |
|  [v1.0.0](#v100)  |

<hr/>

### v1.4.1

* **Actualizadas las dependencias.**
  - discord.py (2.1.0 → **2.2.2**)
  - python-dotenv (0.2.1 → **1.0.0**)

* **Uso de `typing.Union` en vez de `|`** para un poco retrocompatibilidad.

<hr style="height:2px" />

## v1.4.0

* Arreglados bugs con el menu de `/ej`, en donde el menu de unidades no funcionaba para las unidades `2` y `12`.
* **Actualizada la versión de la guía.** Ahora utiliza la revisión del 6 de Marzo de 2022 bajo el nombre `1c2022`.
  - Cambiada *una* palabra del ejercicio **1.6.b)**.
  - Expandido el enunciado del ejercicio **7.11**.
  - Nuevo ejercicio **7.13**.
* **Comando `/meme` removido.** Cayó en desuso y no era rentable mantener las claves.
* **Comandos `/whatsnew` y `/rps` removidos.**
* **Mejorada la lógica de archivos.** Ahora usan búsqueda recursiva e instancias de la clase `pathlib.Path`, en vez de las funciones de `os.path`.
* **Ahora se usa una DB de SQLite3,** en vez de un módulo de constantes.

<hr style="height:4px" />

## v1.3.0

* Puesto que [discord.py](https://github.com/Rapptz/discord.py) ha continuado su mantenimiento, y las *features* que promete traer son preferidas, **se ha decidido en buena fe volver a usar esta librería.**

* **Agregados los *slash commands*.**

* **Agregado nuevo comando `reboot`.** Ahora se puede reiniciar el bot sin tener que apagarlo manualmente.

<hr style="height:4px" />

### v1.2.1

* **Simplificados algunos imports en las pruebas y en el main.** No deberían tener nombres redundantes.
* **Agregados scripts ejecutables.** Ahora debería ser más intuitivo correr el bot.

<hr style="height:2px" />

## v1.2.0

* **Migración a Pycord.** La librería que se venía usando, [discord.py](https://github.com/Rapptz/discord.py), cesó su mantenimiento, y por lo
tanto el bot migró a usar [pycord](https://github.com/Pycord-Development/pycord), un *fork* de discord.py casi idéntico y más actualizado.

* **Reformados los comandos.** Ahora hace uso de `Cogs` para mejor organización de los mismos.

* **Modularización.** Siguiendo la mejora de solidez técnica descrita arriba, muchas funciones
y clases fueron separadas en sus propios módulos.

* **Algunos Comandos ahora usan `Embeds`.** Esto permite una presentación más prolija.

<hr style="height:4px" />

## v1.1.0

Esta versión introduce una nueva imagen para el bot, manejo de imágenes por
Imgur, para mejor experiencia de memes. También se introducen menús contextuales para `ej` y `guia`.

* **¡Nuevo Logo!** Las referencias se encuentran en la carpeta de [imágenes](img).

* **Hace uso de [`imgur-python`](https://pypi.org/project/imgur-python/)** para manejar imágenes a través del bot de Discord.

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

<hr style="height:4px" />

### v1.0.4

Esta versión tiene más que nada mantenimiento y mejoras internas:

* **Mejorada la forma de registrar eventos.** Ahora hace uso del módulo `logging` para registrar eventos en la ejecución del bot.

* **Nuevo archivo** `lector.log` para guardar dichos registros.

<hr style="height:2px" />

### v1.0.3

* **Agregado una actividad `!info`** en el estado del bot.

* **Agregados nuevos mensajes de error** para excepciones del comando `ej`.

<hr style="height:2px" />

### v1.0.2

* **Mejorado un poco el código.** Ahora el cuerpo del código sigue mejor las convenciones de python.
* **Agregadas** algunas que otras palabras nuevas que pueden tocar en el ahorcado.

<hr style="height:2px" />

### v1.0.1

* **Agregado comando `clear`** para limpiar mensajes del bot.

<hr style="height:4px" />

## v1.0.0

* Ahora el bot proviene de una clase `CustomBot` que sobrecarga a la clase de Discord `commands.Bot`. Esto es para contener información persistente, pero los
  comandos siguen siendo definidos mediante decoradores.

* Mejoradas las *type hints* de varias funciones y la documentación en general.

* La estructura del lector de la guía es más flexible y configurable y no depende de valores *hardcodeados* como antes.

* **Nuevo comando `prefix`** con el que cambiar el prefijo del comando. Puede configurarse por separado para cada servidor.

* **Nuevo comando `guia`** con el que configurar la revisión de la guía de ejercicios a utilizar (por defecto actualmente se utiliza la versión `2c2019`).
  De nuevo, la configuración de cada servidor es independiente de las otras. Por ahora la única versión disponible es `2c2019`, pero añadido está el soporte para
  futuras revisiones de la guía.

* Ahora el comando `info` muestra también la versión de la guía.

* **Aún más** memes. *Muuuchos más*.

* **¡Introducido el juego 'hanged' (ahorcado)!**. Se invoca mediante el nuevo comando `hanged` o su alias `ahorcado`. Hace uso de los nuevos hilos en Discord, 
  introducidos en la API 2.0.

* El juego de ahorcado tiene su propia clase, en un archivo separado, y los datos de las partidas se mantienen dentro de la clase `CustomBot`. Hace uso de un
  archivo `.txt` separado para generar las palabras.

* `meme` ahora soporta también que se le pase el ID del meme, por si se quiere uno en concreto (aunque no funciona si el link no comienza con `https://i.imgur.com`)