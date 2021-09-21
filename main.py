import os
from lector import bot

TOKEN = os.environ["DISCORD_TOKEN"]

def main():

    lector = bot
    lector.run(TOKEN)

    return 0

if __name__ == "__main__":

    main()