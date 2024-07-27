from pathlib import Path
import sys
import time
import discord
import json
import discord
import os
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv(dotenv_path="config")
#Les intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

liste_mot_blacklist = ["débile", "nul", "..."]

reponse_gros_mots = [
    "Oh ton langage {} ! C'est pas la cité ici donc parle bien.",
    "Tu parles mal {} il va falloir te calmer !",
    "Tu es bien grossier dis donc {} !",
    "Orhhhhhhh {} je vais devoir te dire combien de fois de te calmer !?"
]

#Création du client avec ses intents
client = discord.Client(intents=intents)

#Le décorateur @client.event permet d'indiquer que la fonction on_ready est
#une fonction qui doit recevoir les informations envoyées lorsque l'événement est appelé par Discord.
@client.event
async def on_ready():
    print("Bot en ligne !")


@client.event
async def on_message(message: discord.Message):
    for mot_blacklist in liste_mot_blacklist:
        if mot_blacklist in message.content.lower():
            print("insulte présent")
            await message.reply(random.choice(reponse_gros_mots).format(message.author.mention))
            await message.delete()
            return

        elif "@everyone" in message.content.lower() and 1031184414476087297 not in [i.id for i in message.author.roles]:  # type: ignore
            print("@everyone présent")
            await message.reply(f"{message.author.mention} ne mentionne pas tout le monde s'il te plait ça dérange tout le monde...")
            await message.delete()
            return



    if message.content.split(" ")[-1].lower() == "quoi":
        await message.reply("FEUR !")
        return




client.run(os.getenv("TOKEN1"))
