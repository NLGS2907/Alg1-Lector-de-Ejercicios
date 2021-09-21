import os

from dotenv import load_dotenv

import lector

load_dotenv("data.env")
TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":

    lector = lector.bot
    lector.run(TOKEN)