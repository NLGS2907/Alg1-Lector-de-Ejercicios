#pylint: disable=line-too-long
"""
Módulo Principal

Permisos necesarios: 'Send Messages' - 'Manage Messages' - "Read Message History" - 'Send Messages in Threads' - 'Manage Threads' - 'Mention Everyone' - 'View Channels' - 'Add Reactions'

Permissions Integer: 292057984064

Enlace para invitar bot: https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=292057984064&scope=bot
Repositorio: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios

[12/28/21] Reboot requerido.
[01/12/22] Reboot requerido.
[02/11/22] Reboot requerido.
[03/14/22] Reboot requerido.
[04/21/22] Reboot requerido.
"""

from .constantes import TOKEN
from .lector import Lector


def main() -> int:
    "Función principal."

    Lector().run(TOKEN)
    return 0


if __name__ == "__main__":

    main()
