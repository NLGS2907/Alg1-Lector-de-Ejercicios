import os
import lector

TOKEN = os.environ["DISCORD_TOKEN"]

def main():

    lector = lector.bot
    lector.run(TOKEN)

    return 0

if __name__ == "__main__":

    main()