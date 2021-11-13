
"""
Módulo Principal

Permisos necesarios: 'Send Messages' - 'Manage Messages' - "Read Message History" - 'Send Messages in Threads' - 'Manage Threads' - 'Mention Everyone' - 'View Channels' - 'Add Reactions'

Permissions Integer: 292057984064

Enlace para invitar bot: https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=292057984064&scope=bot
Repositorio: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios
"""

import os

from dotenv import load_dotenv
load_dotenv()

from lector import bot

TOKEN = os.getenv("DISCORD_TOKEN")

def main():

    bot.run(TOKEN)

    return 0


if __name__ == "__main__":

    main()
