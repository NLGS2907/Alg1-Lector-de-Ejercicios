"""
VERSION = v0.5.0

Módulo Principal

Permisos necesarios: 'Send Messages' - 'Send Messages in Threads' - 'Mention Everyone' - 'View Channels' - 'Add Reactions'

Permisions Integer: 274878073920

Enlace para invitar bot: https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=274878041152&scope=bot
Repositorio: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios
"""

import os

from dotenv import load_dotenv
load_dotenv()

from lector import bot

TOKEN = os.getenv("DISCORD_TOKEN")

def main():

    lector = bot
    lector.run(TOKEN)

    return 0

if __name__ == "__main__":

    main()