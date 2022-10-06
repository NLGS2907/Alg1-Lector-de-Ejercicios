#pylint: disable=line-too-long
"""
Módulo Principal

Permisos necesarios: 'Send Messages' - 'Manage Messages' - "Read Message History" -
                     'Send Messages in Threads' - 'Manage Threads' - 'Mention Everyone' -
                     'Read Messages/View Channels' - 'Add Reactions' - 'Use Slash Commands'

Permissions Integer: 19327560768

Enlace para invitar bot: https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=294205467712&scope=bot%20applications.commands
Repositorio: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios

[12/28/21] Reboot requerido.
[01/12/22] Reboot requerido.
[02/11/22] Reboot requerido.
[03/14/22] Reboot requerido.
[04/21/22] Reboot requerido.
[04/21/22] Segundo Reboot requerido.
[04/21/22] Tercer Reboot requerido.
[04/24/22] Reboot requerido.
[08/07/22] Reboot Requerido.
[01/08/22] Reboot Manual Requerido.
[09/05/22] Reboot Manual.
[09/29/22] Reboot.
[10/01/22] Reboot.
[10/06/22] Reboot.
"""

from .constantes import TOKEN
from .lector import Lector


def main() -> int:
    "Función principal."

    Lector().run(TOKEN)
    return 0


if __name__ == "__main__":

    main()
