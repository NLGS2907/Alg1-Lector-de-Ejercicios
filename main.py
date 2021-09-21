"""
VERSION = v0.5.0

Módulo Principal

Enlace para invitar bot: https://discord.com/api/oauth2/authorize?client_id=889312376036425810&permissions=274877974592&scope=bot
Repositorio: https://github.com/NLGS2907/Alg1-Lector-de-Ejercicios
"""

import os

from dotenv import load_dotenv
load_dotenv()

from lector import bot

TOKEN = os.environ["DISCORD_TOKEN"]

def main():

    lector = bot
    lector.run(TOKEN)

    return 0

if __name__ == "__main__":

    main()