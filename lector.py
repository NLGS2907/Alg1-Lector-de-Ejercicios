import os

from dotenv import load_dotenv
from discord.ext import commands

import guia

load_dotenv("data.env")
TOKEN = os.getenv("DISCORD_TOKEN")
CMD_PREFIX = os.getenv("CMD_PREFIX")

GUIA = guia.cargar_guia()

bot = commands.Bot(command_prefix=CMD_PREFIX)

@bot.event
async def on_ready():

    print(f"-=-\n{bot.user}, ¡Está conectado y listo!\n-=-")

@bot.command(name="ej", help="Lee ejercicios de la guía.")
async def leer_ejercicio(ctx, unidad: str, ejercicio: str):

    if 1 <= int(unidad) <= 17:

        enunciado = GUIA[unidad].get(ejercicio, '')

        if enunciado:

            await ctx.channel.send(f"**{ctx.author.mention}** ha consultado:\n\n>>> **Unidad** {unidad} - \"{GUIA[unidad]['titulo']}\"  |  **Ejercicio** {ejercicio}:\n\n**{unidad}.{ejercicio}.** {enunciado}")

# @bot.command(name="shutdown", help=f"Desconecta el bot. (Sólo el dueño ({bot.owner_id}) puede usar esto).")
# @commands.is_owner()
# async def shutdown(ctx):

#     bot.logout()