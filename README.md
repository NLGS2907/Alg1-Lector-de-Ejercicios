# Lector de Ejercicios

Este bot de discord está pensado para usarse únicamente en el discord de la materia Algoritmos y Programación I,
de la Facultad de Ingeniería de la UBA, aunque puede utilizarse para cualquier servidor que lo quiera.

**Enlace de Invitación:** [Aquí](https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=292057984064&scope=bot)

<hr/>

### ⋆ [Changelog] Nuevo en v1.0.2

* **Mejorado un poco el código.** Ahora el cuerpo del código sigue mejor las convenciones de python.
* **Agregadas** algunas que otras palabras nuevas que pueden tocar en el ahorcado.
### ⋆ [Changelog] Nuevo en v1.0.1

* **Agregado comando `clear`** para limpiar mensajes del bot.

### ⋆ [Changelog] Nuevo en v1.0.0

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