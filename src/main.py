
"""
Módulo Principal

Permisos necesarios: 'Send Messages' - 'Manage Messages' - "Read Message History" - 'Send Messages in Threads' - 'Manage Threads' - 'Mention Everyone' - 'View Channels' - 'Add Reactions'

Permissions Integer: 292057984064

Enlace para invitar bot: https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=292057984064&scope=bot
Repositorio: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios

[12/28/21] Reboot requerido.
[01/12/22] Reboot requerido.
"""

from constantes import TOKEN

from lector import bot, log

def main():

    bot.run(TOKEN)

    log.info(f"{bot.user} se desconectó satisfactoriamente.\n")

    return 0


if __name__ == "__main__":

    main()
