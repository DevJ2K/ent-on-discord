import discord
import json
from entClass import Ent
from gestion_data import Data
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View
import os  
from dotenv import load_dotenv
load_dotenv(dotenv_path="config")


intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.typing = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


all_user_online = {}
def add_user_online(all_user_online):
    with open("user_online.json", "w") as f:
        json.dump(all_user_online, f, indent=4)

add_user_online(all_user_online)


def get_user_online():
    with open("user_online.json", "r") as f:
        return json.load(f)

user_online = get_user_online()


def verifier_connexion(discordId: int):
    if discordId not in user_online or user_online[discordId][1] == False:
        user_online[discordId] = [Ent(), True]
        all_user_online[discordId] = True
        user_online[discordId][0].connexion(discordId)
        print("Connexion effectué")
        add_user_online(all_user_online)


@bot.event
async def on_ready():
    print("Le bot est prêt !")

@bot.event
async def on_raw_typing(payload: discord.RawTypingEvent):
    if payload.channel_id != 1033896513467842611: #Si ce n'est pas dans le channel "test-commands"
        return

    verifier_connexion(payload.user_id)





@bot.command(name="connexion")
async def connexion(ctx: commands.context.Context):
    user_online[ctx.author.id][0].connexion(ctx.author.id)


@bot.command(name="getMoyenneG") 
async def getMoyenneGenerale(ctx: commands.context.Context): #parametre(show) permet de montrer à tout le monde sa commande
    
    moyenne = user_online[ctx.author.id][0].getMoyenneGenerale()
    
    embed = discord.Embed(title="Moyenne Générale", description="Votre moyenne générale.", color=0x00FE23, url="")
    myn_eleve = float(moyenne[0].split(":")[1][1:].replace(",", "."))
    myn_classe = float(moyenne[1].split(":")[1][1:].replace(",", "."))
    embed.add_field(name="Élève", value=myn_eleve, inline=True)
    embed.add_field(name="Classe", value=myn_classe, inline=True)

    if myn_eleve > myn_classe:
        embed.set_footer(text="Vous êtes au dessus de la moyenne de classe !")
    elif myn_eleve < myn_classe:
        embed.set_footer(text="Vous êtes en dessous de la moyenne de classe !")
    elif myn_eleve == myn_classe:
        embed.set_footer(text="Votre moyennne est égale à la moyenne de classe !")

    await ctx.reply(embed=embed)

@bot.command(name="getAllMoyennes")
async def getAllMoyennes(ctx: commands.context.Context):
    all_moyennes = user_online[ctx.author.id][0].getAllMoyennes()

    embed = discord.Embed(title="Toutes Vos Moyennes", description="Toutes vos moyennes dans vos matières.", color=0x00FE23, url="")

    for moyenne in all_moyennes:
        embed.add_field(name=moyenne[0], value=moyenne[1], inline=False)

    await ctx.reply(embed=embed)



@bot.command(name="getEDT")
async def getEmploiDuTemps(ctx: commands.context.Context):
    edt = user_online[ctx.author.id][0].getEmploiDuTemps()
    
    embed = discord.Embed(title=f"Vos cours de : {edt[0]}", description=f"Votre emploi du temps de : {edt[0]}", color=0x00FE23, url="")

    for cours in edt[1]:
        cours[1] = "\n".join(cours[1]) + "\n--------------------"
        embed.add_field(name=cours[0], value=cours[1], inline=False)


    await ctx.reply(embed=embed)


@bot.command(name="getLastNotes")
async def lastNotes(ctx: commands.context.Context):
    all_notes = user_online[ctx.author.id][0].lastNotes()

    embed = discord.Embed(title=f"Vos {(len(all_notes))//2} Dernières Notes", description="Vos dernières notes visibles sur la page d'accueil de Pronote.", color=0x00FE23, url="")

    for i in range(len(all_notes)):
        if i%2==0:
            embed.add_field(name=all_notes[i], value=all_notes[i+1], inline=False)

    await ctx.reply(embed=embed)


@bot.command(name="getAllDevoirs")
async def getAllDevoirs(ctx: commands.context.Context):
    all_devoirs = user_online[ctx.author.id][0].getAllDevoirs()

    embed = discord.Embed(title=f"Tous Vos Devoirs", description="Tous vos prochains devoirs visibles sur la page d'accueil de Pronote.", color=0x00FE23, url="")
    liste_embed = []
    for journee in all_devoirs:
        temp = discord.Embed(title=f"{journee[0]}", color=0x00FE23, url="")

        pos_fait_non_fait = []
        bloc_devoir = []

        for chaine in range(len(journee)):
            if journee[chaine] in ["Non Fait", "Fait"]:
                pos_fait_non_fait.append(chaine)


        for i in pos_fait_non_fait:
            if journee[i] in ["Fait", "Non Fait"]:
                bloc_devoir.append([journee[i-1], journee[i]])


        for i in pos_fait_non_fait:
            cours = ""
            try:
                next_i = pos_fait_non_fait[pos_fait_non_fait.index(i)+1]
            except IndexError:
                if len(journee)-1 == i:
                    cours = "..."
                else:
                    for y in range(i+1, len(journee)):
                        cours += f"{journee[y]}\n"
                
                bloc_devoir[pos_fait_non_fait.index(i)].append(cours)
                break

            if next_i - i == 2:
                cours = "..."
            else:
                for y in range(i+1, next_i-1):
                    cours += f"{journee[y]}\n"

            bloc_devoir[pos_fait_non_fait.index(i)].append(cours)

        for cours_ in bloc_devoir:
            temp.add_field(name=f"{cours_[0]} -> {cours_[1]}", value=cours_[2], inline=False)

        liste_embed.append(temp)


    await ctx.reply(embeds=liste_embed)




@bot.command(name="del")
async def delete(ctx, number_of_messages: int):
    messages = [ctx async for ctx in ctx.channel.history(limit=number_of_messages + 1)]

    for each_message in messages:
        await each_message.delete()


@bot.command(name="register")
async def register(ctx: commands.context.Context, ENTid: str):
    messages = [ctx async for ctx in ctx.channel.history(limit=1)]
    await messages[0].delete()
    listIdMdp = ENTid.split("|")
    database = Data()
    database.write_new_user(ctx.author.id, listIdMdp[0], listIdMdp[1])


# user.connexion(203272768844857353)
bot.run(os.getenv("TOKEN1"))