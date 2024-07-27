from pathlib import Path
import sys
import time
import discord
import json
from entClass import Ent
from gestion_data import Data
from nextcord.ext import commands
from nextcord.utils import get
from nextcord import ButtonStyle, SelectOption
from nextcord.ui import Button, View, Modal, Select
import os  
from dotenv import load_dotenv
load_dotenv(dotenv_path="config")


intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.typing = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)




user_online = {}


def connect_user(discordId: int):
    if not verification_online_user(discordId):
        user_online[discordId] = [Ent(), True]
        user_online[discordId][0].connexion(discordId)
        print("Connexion effectué")
    
        

def verification_online_user(discordId: int):
    if discordId not in user_online or user_online[discordId][1] == False:
        return False
    else:
        return True

# ===================================================================================================
# CALLBACK FONCTION
# ===================================================================================================

async def edtButton_callback(interaction: discord.Interaction):
        
    if not verification_online_user(interaction.user.id):       #type: ignore
        await interaction.response.send_message("Connexion en cours... Recliquez sur le bouton lorsque ce message aura disparu...", ephemeral=True)
        connect_user(interaction.user.id)       #type: ignore
        await interaction.delete_original_message()
        
    else:

        choiceDayView = View(timeout=None)

        choiceDayView.add_item(previousDayButton)
        choiceDayView.add_item(nextDayButton)

        edt = user_online[interaction.user.id][0].getEmploiDuTemps()       #type: ignore
        if edt[0] == False:
            await interaction.response.send_message(f"Vous n'avez pas cours le : {edt[1]}", view=choiceDayView, ephemeral=True)
            return

        embed = discord.Embed(title=f"Vos cours de : {edt[0]}", description=f"Votre emploi du temps de : {edt[0]}", color=0x20FFF5, url="")

        for cours in edt[1]:
            cours[1] = "\n".join(cours[1]) + "\n──────────────"
            if len(cours[0]) == 1:
                cours[0] = "À " + cours[0][0] + " :"
            else:
                cours[0] ="De "+" à ".join(cours[0])+" :"

            if cours[1]=="\n──────────────" or "Pas de cours" in cours[1]:
                cours[1] = "Pas de cours" + "\n──────────────"
                embed.add_field(name=cours[0], value=cours[1], inline=False)
            else:
                embed.add_field(name=cours[0], value=cours[1], inline=False)


        

        

        await interaction.response.send_message(embed=embed, view=choiceDayView, ephemeral=True)

async def nextDayEdtButton_callback(interaction: discord.Interaction):
    await interaction.response.defer()
     
    choiceDayView = View(timeout=None)
    choiceDayView.add_item(previousDayButton)
    choiceDayView.add_item(nextDayButton)

    edt = user_online[interaction.user.id][0].nextDayEDT()     #type: ignore

    if edt == False:
        choiceDayView.remove_item(nextDayButton)
        await interaction.delete_original_message()
        await interaction.followup.send(f"Vous avez atteint la limite des jours affichés sur Pronote.", view=choiceDayView, ephemeral=True)
        return

    elif edt[0] == False:
        await interaction.delete_original_message()
        await interaction.followup.send(f"Vous n'avez pas cours le : {edt[1]}", view=choiceDayView, ephemeral=True)
        return

    

    embed = discord.Embed(title=f"Vos cours de : {edt[0]}", description=f"Votre emploi du temps de : {edt[0]}", color=0x20FFF5, url="")

    for cours in edt[1]:
        cours[1] = "\n".join(cours[1]) + "\n──────────────"
        if len(cours[0]) == 1:
            cours[0] = "À " + cours[0][0] + " :"
        else:
            cours[0] ="De "+" à ".join(cours[0])+" :"

        if cours[1]=="\n──────────────" or "Pas de cours" in cours[1]:
            cours[1] = "Pas de cours" + "\n──────────────"
            embed.add_field(name=cours[0], value=cours[1], inline=False)
        else:
            embed.add_field(name=cours[0], value=cours[1], inline=False)

    await interaction.delete_original_message()
    await interaction.followup.send(embed=embed, view=choiceDayView, ephemeral=True)
 
async def previousDayEdtButton_callback(interaction: discord.Interaction):
    await interaction.response.defer()
    

    choiceDayView = View(timeout=None)
    choiceDayView.add_item(previousDayButton)
    choiceDayView.add_item(nextDayButton)

    edt = user_online[interaction.user.id][0].previousDayEDT()     #type: ignore

    if edt == False:
        choiceDayView.remove_item(previousDayButton)
        await interaction.delete_original_message()
        await interaction.followup.send(f"Vous avez atteint la limite des jours affichés sur Pronote.", view=choiceDayView, ephemeral=True)
        return

    elif edt[0] == False:
        await interaction.delete_original_message()
        await interaction.followup.send(f"Vous n'avez pas cours le : {edt[1]}", view=choiceDayView, ephemeral=True)
        return

    

    embed = discord.Embed(title=f"Vos cours de : {edt[0]}", description=f"Votre emploi du temps de : {edt[0]}", color=0x20FFF5, url="")

    for cours in edt[1]:
        cours[1] = "\n".join(cours[1]) + "\n──────────────"
        if len(cours[0]) == 1:
            cours[0] = "À " + cours[0][0] + " :"
        else:
            cours[0] ="De "+" à ".join(cours[0])+" :"

        if cours[1]=="\n──────────────" or "Pas de cours" in cours[1]:
            cours[1] = "Pas de cours" + "\n──────────────"
            embed.add_field(name=cours[0], value=cours[1], inline=False)
        else:
            embed.add_field(name=cours[0], value=cours[1], inline=False)

    await interaction.delete_original_message()
    await interaction.followup.send(embed=embed, view=choiceDayView, ephemeral=True)
      
async def allDevoirsButton_callback(interaction: discord.Interaction):
    if not verification_online_user(interaction.user.id):       #type: ignore
        await interaction.response.send_message("Connexion en cours... Recliquez sur le bouton lorsque ce message aura disparu...", ephemeral=True)
        connect_user(interaction.user.id)       #type: ignore
        await interaction.delete_original_message()

    else:
        all_devoirs = user_online[interaction.user.id][0].getAllDevoirs()       #type: ignore

        embed = discord.Embed(title=f"Tous Vos Devoirs", description="Tous vos prochains devoirs visibles sur la page d'accueil de Pronote.", color=0xFF0000, url="")
        liste_embed = [embed]
        for journee in all_devoirs:
            temp = discord.Embed(title=f"{journee[0]}", color=0xFF9B13, url="")

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
                temp.add_field(name=f"{cours_[0]} → {cours_[1]}", value=cours_[2], inline=False)

            liste_embed.append(temp)


        
        await interaction.response.send_message(embeds=liste_embed, ephemeral=True)

async def lastNotesButton_callback(interaction: discord.Interaction):
    if not verification_online_user(interaction.user.id):       #type: ignore
        await interaction.response.send_message("Connexion en cours... Recliquez sur le bouton lorsque ce message aura disparu...", ephemeral=True)
        connect_user(interaction.user.id)       #type: ignore
        await interaction.delete_original_message()

    else:
        all_notes = user_online[interaction.user.id][0].lastNotes()       #type: ignore
        if (len(all_notes)//2) == 0:
            await interaction.response.send_message("Vous n'avez aucune nouvelle note.", ephemeral=True)
            return
        elif (len(all_notes)//2) == 1:
            embed = discord.Embed(title=f"Votre Dernière Note", description="Votre dernière note visible sur la page d'accueil de Pronote.", color=0x1365FF, url="")
        else:
            embed = discord.Embed(title=f"Vos {(len(all_notes))//2} Dernières Notes", description="Vos dernières notes visibles sur la page d'accueil de Pronote.", color=0x1365FF, url="")

        for i in range(len(all_notes)):
            if i%2==0:
                embed.add_field(name=all_notes[i], value=all_notes[i+1]+"\n──────────────", inline=False)


        await interaction.response.send_message(embed=embed, ephemeral=True)
        
async def moyenneGeneraleButton_callback(interaction: discord.Interaction):
    if not verification_online_user(interaction.user.id):       #type: ignore
        await interaction.response.send_message("Connexion en cours... Recliquez sur le bouton lorsque ce message aura disparu...", ephemeral=True)
        connect_user(interaction.user.id)       #type: ignore
        await interaction.delete_original_message()
    
    else:
        moyenne = user_online[interaction.user.id][0].getMoyenneGenerale()       #type: ignore

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


        await interaction.response.send_message(embed=embed, ephemeral=True)    

async def allMoyennesButton_callback(interaction: discord.Interaction):
    if not verification_online_user(interaction.user.id):       #type: ignore
        await interaction.response.send_message("Connexion en cours... Recliquez sur le bouton lorsque ce message aura disparu...", ephemeral=True)
        connect_user(interaction.user.id)       #type: ignore
        await interaction.delete_original_message()
    else:
        all_moyennes = user_online[interaction.user.id][0].getAllMoyennes()       #type: ignore

        embed = discord.Embed(title="Toutes Vos Moyennes", description="Toutes vos moyennes dans vos matières.", color=0xFFBF13, url="")

        for moyenne in all_moyennes:
            embed.add_field(name=moyenne[0], value=moyenne[1]+ "\n──────────────", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True) 

async def registerButton_callback(interaction: discord.Interaction):
    ticket = discord.utils.get(interaction.guild.text_channels, name=f"connexion-pour-{interaction.user.name}-{interaction.user.discriminator}") #type: ignore
    if ticket is not None:
        await interaction.response.send_message(f"Oh, tu as déjà un channel de connexion pour toi ici -> {ticket.mention} !", ephemeral=True)
    else:
        permission = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),       #type: ignore
            interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)       #type: ignore
        }

        #CREATION DU TICKET
        def checkMessage(message: discord.Message):
            return message.author.id == interaction.user.id        #type: ignore

        channel_ticket = await interaction.guild.create_text_channel(name=f"connexion-pour-{interaction.user.name}-{interaction.user.discriminator}", overwrites=permission, reason=f"Ticket de connexion de {interaction.user}")  # type: ignore
        await interaction.response.send_message(f"Le ticket te permettant de te connecter a bien été créé ici -> {channel_ticket.mention} !", ephemeral=True)
        embed = discord.Embed(title=f"Assistance De Connexion", description=f"Salut {interaction.user.mention} ! ", color=0x00FE23, url="")       #type: ignore
        with open("toutesLesTxt/register1.txt", "r", encoding="utf-8") as f:
            mot ="".join(f.readlines())
        await channel_ticket.send(f"{mot}".format(interaction.user.mention, bot.user.id, bot.get_channel(1036065317778112522).mention))       #type: ignore
        
        identifiantDict = {}

        try:
            input_id = await bot.wait_for("message", timeout=180, check=checkMessage)
            identifiantDict['id'] = input_id.content.lower()

        except:
            await bot.get_channel(channel_ticket.id).delete()       #type: ignore
            print("Erreur")
            return
        

        try:
            await channel_ticket.send(f"Ok, maintenant quelle est ton mot de passe ? (ne t'inquiète pas je suis le seul à pouvoir le voir, ça reste entre nous ;)") 
            input_mdp = await bot.wait_for("message", timeout=180, check=checkMessage)
            identifiantDict['mdp'] = input_mdp.content
            await input_mdp.delete()
            await channel_ticket.send(f"#"*len(input_mdp.content))

        except:
            await bot.get_channel(channel_ticket.id).delete()       #type: ignore
            print("Erreur")
            return

        def create_embed(new_user_id, new_user_mdp):
            embed = discord.Embed(title=f"Vos Identifiants", color=0x00FE23, url="")
            embed.add_field(name="Identifiant", value=f"__{new_user_id}__")
            embed.add_field(name="Mot de passe", value=f"||{new_user_mdp}|| ***← Cliquez pour voir !***")
            return embed

        async def correctId_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            print(identifiantDict['id'], identifiantDict['mdp'])
            await channel_ticket.send(f"Nickel {interaction.user.mention} ! On arrive au moment final, je vais essayer de me connecter à l'ENT avec tes identifiants, si j'y arrive tu auras l'accès à tous les salons sinon tu vas devoir re-vérifier tes identifiants...")        #type: ignore
            await channel_ticket.send(f"Tentative de connexion en tant que '{identifiantDict['id']}' en cours...")

            Data().write_new_user(interaction.user.id, identifiantDict['id'], identifiantDict['mdp'])        #type: ignore
            status_connexion = Ent().connexion(interaction.user.id)        #type: ignore
            if status_connexion == "successful":
                print("Connexion réussie")
                
                eleve_role = interaction.guild.get_role(1031185341383716935)       #type: ignore
                arrivant_role = interaction.guild.get_role(1036037404345245756)    #type: ignore 

                await channel_ticket.send(f"Parfait la connexion s'est parfaitement déroulée ! Je te met le rôle '{eleve_role.mention}' qui va te permettre de voir tous les salons !")        #type: ignore


                async def endButton_callback(interaction: discord.Interaction):
                    if eleve_role not in interaction.user.roles:       #type: ignore
                        await interaction.user.add_roles(eleve_role)       #type: ignore
                        await interaction.user.remove_roles(arrivant_role)       #type: ignore

                    await interaction.channel.delete()       #type: ignore

                endButton = Button(label="Découvrir !", style=ButtonStyle.blurple)
                endButton.callback = endButton_callback
                endView = View()
                endView.add_item(endButton)

                with open("toutesLesTxt/register2.txt", "r", encoding="utf-8") as f:
                    mot ="".join(f.readlines())
                await channel_ticket.send(f"{mot}".format(interaction.user.mention), view=endView)       #type: ignore

            elif status_connexion == "mdp_incorrect":
                await channel_ticket.send("Oh oh, tu t'es trompé dans ton identifiant ou ton mot de passe d'après l'ENT, est-ce que tu peux re-vérifier tes identifiants s'il te plaît ?")
                await channel_ticket.send("Est-ce que tout est correct ?",embed=create_embed(identifiantDict['id'], identifiantDict['mdp']), view=myView)

            elif status_connexion == "fail_server":
                await channel_ticket.send("Oh oh, il y a eu un problème sur l'ordinateur hôte... Merci de retenter la connexion ultérieurement.")
                print("Probleme côté serveur")
            else:
                print("Autres")
            

        async def changeId_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await channel_ticket.send("**Ok redonne-moi ton identifiant ENT qui est sous cette forme :** __prenom.nom__")
            try:
                input_id = await bot.wait_for("message", timeout=180, check=checkMessage)
                identifiantDict['id'] = input_id.content.lower()
                await channel_ticket.send("Est-ce que tout est correct ?",embed=create_embed(identifiantDict['id'], identifiantDict['mdp']), view=myView)

            except:
                await bot.get_channel(channel_ticket.id).delete()       #type: ignore


        async def changeMdp_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await channel_ticket.send("**Ok redonne-moi ton mot de passe s'il te plaît :**")
            try:
                input_mdp = await bot.wait_for("message", timeout=180, check=checkMessage)
                identifiantDict['mdp'] = input_mdp.content
                await input_mdp.delete()
                await channel_ticket.send(f"#"*len(input_mdp.content))
                await channel_ticket.send("Est-ce que tout est correct ?",embed=create_embed(identifiantDict['id'], identifiantDict['mdp']), view=myView)

            except:
                await bot.get_channel(channel_ticket.id).delete()       #type: ignore
                return



        correctButton = Button(label="Valider", style=ButtonStyle.blurple)
        changeIdButton = Button(label="Changer l'Identifiant", style=ButtonStyle.red)
        changeMdpButton = Button(label="Changer le Mot De Passe", style=ButtonStyle.red)

        correctButton.callback = correctId_callback
        changeIdButton.callback = changeId_callback
        changeMdpButton.callback = changeMdp_callback

        myView = View()
        myView.add_item(correctButton) 
        myView.add_item(changeIdButton)
        myView.add_item(changeMdpButton)
        await channel_ticket.send("Est-ce que tout est correct ?",embed=create_embed(identifiantDict['id'], identifiantDict['mdp']), view=myView)

async def refreshButton_callback(interaction: discord.Interaction):
    if not verification_online_user(interaction.user.id):       #type: ignore
        await interaction.response.send_message("Vous n'êtes pas encore connecté(e), une nouvelle connexion est en cours... Une fois ce message disparu, vous pourrez profiter de tous les boutons.", ephemeral=True)
        connect_user(interaction.user.id)       #type: ignore
        await interaction.delete_original_message()
    elif verification_online_user(interaction.user.id):       #type: ignore
        await interaction.response.send_message("Rafraîchissement en cours... Une fois ce message disparu, vous pourrez profiter de-nouveau de tous les boutons.", ephemeral=True)
        user_online[interaction.user.id][0].close()       #type: ignore
        user_online[interaction.user.id][1] = False       #type: ignore
        connect_user(interaction.user.id)       #type: ignore
        await interaction.delete_original_message()

    else:
        await interaction.response.send_message(f"Oh oh, une erreur est survenue ! Merci de te rendre dans la salon {bot.get_channel(1039611828285743226).mention} pour signaler ton problème et qu'il soit réglé.", ephemeral=True)       #type: ignore



class helpModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Besoin D'Aide !"
        )
        self.probleme = discord.ui.TextInput(label="Nom Du Problème", min_length=3, max_length=124, required=True, placeholder="Entrez le thème du problème.", style=discord.TextInputStyle.short)
        self.description = discord.ui.TextInput(label="Description Du Problème", min_length=10, max_length=4000, required=True, placeholder="Décrivez votre problème le plus explicitement possible.", style=discord.TextInputStyle.paragraph)

        self.add_item(self.probleme)
        self.add_item(self.description)

    async def callback(self, interaction: discord.Interaction):
        probleme = self.probleme.value
        description = self.description.value
        numero_demande = 1
        txt_dmd_utilisateur = Path.cwd() / "tous_les_problemes" / f"probleme_numero_{numero_demande}_de_{interaction.user.name}-{interaction.user.discriminator}.txt"      #type: ignore
        while txt_dmd_utilisateur.is_file():
            numero_demande += 1
            txt_dmd_utilisateur = Path.cwd() / "tous_les_problemes" / f"probleme_numero_{numero_demande}_de_{interaction.user.name}-{interaction.user.discriminator}.txt"      #type: ignore

        txt_dmd_utilisateur.touch()

        with open(txt_dmd_utilisateur, "w", encoding="utf-8") as f:
            f.write(f"Nom Du Problème : {probleme}\nDescription Du Problème : {description}")

        embed = discord.Embed(title=f"Problème n°{numero_demande} de {interaction.user.name}-{interaction.user.discriminator}", description=f"Fast Contact : {interaction.user.mention}", color=0xFF0000)      #type: ignore
        embed.add_field(name=probleme, value=description)
        await bot.get_channel(1038662232013283388).send(embed=embed)      #type: ignore


        await interaction.response.send_message(f"Votre problème a bien été envoyé ! Il sera résolu dans les plus brefs délais et vous recevrez un message si nécessaire !", ephemeral=True)


async def helpButton_callback(interaction: discord.Interaction):
    await interaction.response.send_modal(helpModal())     


class suggestionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Suggestions"
        )
        self.suggestion = discord.ui.TextInput(label="Nom De Votre Suggestion", min_length=3, max_length=124, required=True, placeholder="Entrez le thème de votre suggestion.", style=discord.TextInputStyle.short)
        self.description = discord.ui.TextInput(label="Descrivez votre/vos suggestions", min_length=10, max_length=4000, required=True, placeholder="Décrivez votre/vos suggestions le plus explicitement possible.", style=discord.TextInputStyle.paragraph)

        self.add_item(self.suggestion)
        self.add_item(self.description)

    async def callback(self, interaction: discord.Interaction):
        suggestion = self.suggestion.value
        description = self.description.value
        numero_demande = 1
        txt_dmd_utilisateur = Path.cwd() / "toutes_les_suggestions" / f"suggestion_numero_{numero_demande}_de_{interaction.user.name}-{interaction.user.discriminator}.txt"      #type: ignore
        while txt_dmd_utilisateur.is_file():
            numero_demande += 1
            txt_dmd_utilisateur = Path.cwd() / "toutes_les_suggestions" / f"suggestion_numero_{numero_demande}_de_{interaction.user.name}-{interaction.user.discriminator}.txt"      #type: ignore

        txt_dmd_utilisateur.touch()

        with open(txt_dmd_utilisateur, "w", encoding="utf-8") as f:
            f.write(f"Nom De La Suggestion : {suggestion}\nDescription De La Suggestion : {description}")
       
        embed = discord.Embed(title=f"Suggestion n°{numero_demande} de {interaction.user.name}-{interaction.user.discriminator}", description=f"Fast Contact : {interaction.user.mention}",color=0x00FF0F)      #type: ignore
        embed.add_field(name=suggestion, value=description)
        await bot.get_channel(1038662330763972609).send(embed=embed)      #type: ignore

        await interaction.response.send_message(f"Merci de ta suggestion, elle a bien été envoyé ! Un retour vous sera envoyé dans les plus brefs délais !", ephemeral=True)


async def suggestionButton_callback(interaction: discord.Interaction):
    await interaction.response.send_modal(suggestionModal())    
           

class requestsSomethingModal(discord.ui.Modal):
    def __init__(self, channel_use):
        self.channel_use = channel_use
        self.name_channel = "Default"
        super().__init__(
            "Faire Une Demande"
        )
        self.username = discord.ui.TextInput(label="Faire une demande", min_length=2, max_length=124, required=True, placeholder="prenom.nom OU @pseudo(sans les #xxxx)", style=discord.TextInputStyle.short)

        if self.channel_use == 1031318493603303504:
            self.username.label = "Demander l'emploi du temps de"
            self.name_channel = "edt"
                

        elif self.channel_use == 1031318536448127136:
            self.username.label = "Demander les prochains devoirs de"
            print("Prochain devoir")
            self.name_channel = "allDevoirs"
            

        elif self.channel_use == 1031318616374779986:
            self.username.label = "Demander les dernières notes de"
            print("Derniere note")
            self.name_channel = "lastNotes"

        elif self.channel_use == 10359521093985280901111:
            self.username.label = "Demander la moyenne générale de"
            print("Vos moyennes G")
            self.name_channel = "moyenneG"

        elif self.channel_use == 10359521093985280902222:
            self.username.label = "Demander toutes les moyennes de"
            print("Vos moyennes all")
            self.name_channel = "allMoyennes"

        elif self.channel_use == 1035959724421681192:
            self.username.label = "Demander l... de"

        self.add_item(self.username)


    async def callback(self, interaction: discord.Interaction):
        pseudo:str = self.username.value #type: ignore
        self.utilisateur_data = Data().get_user_by_entId(pseudo)
        self.utilisateur_cible = interaction.user


        if pseudo.startswith("@"): #PSEUDO DISCORD
            liste_eleves = []
            for members in bot.get_all_members():

                if members.get_role(1031185341383716935) is not None:
                    liste_eleves.append(members.display_name.lower())
                    
            
            if pseudo[1:].lower() in liste_eleves:
                
                for members in bot.get_all_members():

                    if members.get_role(1031185341383716935) is not None and pseudo[1:].lower() == members.display_name.lower():
                        self.utilisateur_cible = members
                        await self.create_ticket(interaction=interaction)
                        return
                    


        elif self.utilisateur_data != False: #IDENTIFIANT ENT
            if type(self.utilisateur_data) == tuple:
                self.utilisateur_cible = bot.get_user(self.utilisateur_data[0])
                await self.create_ticket(interaction=interaction)
                return
                
            elif type(self.utilisateur_data) == list and len(self.utilisateur_data) >= 2:
                async def selectUser_callback(interactionCall: discord.Interaction):
                    self.utilisateur_cible = bot.get_user(int(selectUser.values[0]))
                    await self.create_ticket(interaction=interactionCall)
                    await interaction.delete_original_message()
                    
                    return
                    

                liste_option = [SelectOption(label=bot.get_user(membre_in_data[0]).display_name, value=f"{membre_in_data[0]}") for membre_in_data in self.utilisateur_data]      #type: ignore
                selectUser = Select(placeholder="Plusieurs utilisateurs sont connectés à ce compte, à qui souhaitez-vous envoyer une demande ?", options=liste_option, max_values=1)
                selectUser.callback = selectUser_callback      #type: ignore
                myView = View(timeout=None)
                myView.add_item(selectUser)
                await interaction.response.send_message(view=myView, ephemeral=True)
                return

        else:
            await interaction.response.send_message(f"L'utilisateur '{pseudo}' est introuvable", ephemeral=True)
            return

    async def create_ticket(self, interaction: discord.Interaction):
        ticket = discord.utils.get(bot.get_all_channels(), name=f"〘❔〙mes-demandes-{self.utilisateur_cible.name.lower()}-{self.utilisateur_cible.discriminator}")      #type: ignore
        
        if ticket is not None:
            pass
        else:
            permission = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),       #type: ignore
                interaction.guild.get_member(self.utilisateur_cible.id): discord.PermissionOverwrite(view_channel = True, send_messages = False, read_message_history = True)       #type: ignore
            }

            ticket = await interaction.guild.create_text_channel(name=f"〘❔〙mes-demandes-{self.utilisateur_cible.name}-{self.utilisateur_cible.discriminator}", overwrites=permission)  # type: ignore



       
        await interaction.response.send_message(f"Votre demande a bien été envoyé à {self.utilisateur_cible.mention} !", ephemeral=True)      #type: ignore

            
        
        async def edtToSend_callback(interactionCallback: discord.Interaction):
            await interactionCallback.response.defer()
            await interactionCallback.message.delete()      #type: ignore
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:      #type: ignore
                await interactionCallback.channel.delete()      #type: ignore

            await interaction.user.send(f"**Ta demande a bien été accepté par {self.utilisateur_cible.mention} ! Tu recevras ce que tu as demandé dans quelques secondes...**")      #type: ignore

            if not verification_online_user(self.utilisateur_cible.id):       #type: ignore
                connect_user(self.utilisateur_cible.id)       #type: ignore
                
            edt = user_online[self.utilisateur_cible.id][0].getEmploiDuTemps()       #type: ignore
            if edt[0] == False:
                await interaction.user.send(f"{self.utilisateur_cible.display_name.capitalize()} n'a pas cours le : {edt[1]}")      #type: ignore
                return
        
            embed = discord.Embed(title=f"Les cours de {self.utilisateur_cible.display_name.capitalize()} pour : {edt[0]}", description=f"L'emploi du temps de <@{self.utilisateur_cible.id}> pour : {edt[0]}", color=0x00FFF5, url="")       #type: ignore

            for cours in edt[1]:
                cours[1] = "\n".join(cours[1]) + "\n──────────────"
                if len(cours[0]) == 1:
                    cours[0] = "À " + cours[0][0] + " :"
                else:
                    cours[0] ="De "+" à ".join(cours[0])+" :"

                if cours[1]=="\n──────────────" or "Pas de cours" in cours[1]:
                    cours[1] = "Pas de cours" + "\n──────────────"
                    embed.add_field(name=cours[0], value=cours[1], inline=False)
                else:
                    embed.add_field(name=cours[0], value=cours[1], inline=False)


            await interaction.user.send(embed=embed)      #type: ignore

        async def allDevoirsToSend_callback(interactionCallback: discord.Interaction):
            await interactionCallback.response.defer()
            await interactionCallback.message.delete()      #type: ignore
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:      #type: ignore
                await interactionCallback.channel.delete()      #type: ignore

            await interaction.user.send(f"**Ta demande a bien été accepté par {self.utilisateur_cible.mention} ! Tu recevras ce que tu as demandé dans quelques secondes...**")      #type: ignore

            if not verification_online_user(self.utilisateur_cible.id):       #type: ignore
                connect_user(self.utilisateur_cible.id)       #type: ignore

        
            all_devoirs = user_online[self.utilisateur_cible.id][0].getAllDevoirs()       #type: ignore

            embed = discord.Embed(title=f"Tous Les Devoirs de {self.utilisateur_cible.display_name.capitalize()}", description=f"Les prochains devoirs de <@{self.utilisateur_cible.id}> visibles sur la page d'accueil de Pronote.", color=0xFF0000, url="")      #type: ignore
            liste_embed = [embed]
            for journee in all_devoirs:
                temp = discord.Embed(title=f"{journee[0]}", color=0xFF9B13, url="")

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


            
            await interaction.user.send(embeds=liste_embed)      #type: ignore

        async def lastNotesToSend_callback(interactionCallback: discord.Interaction):
            await interactionCallback.response.defer()
            await interactionCallback.message.delete()      #type: ignore
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:      #type: ignore
                await interactionCallback.channel.delete()      #type: ignore

            await interaction.user.send(f"**Ta demande a bien été accepté par {self.utilisateur_cible.mention} ! Tu recevras ce que tu as demandé dans quelques secondes...**")      #type: ignore

            if not verification_online_user(self.utilisateur_cible.id):       #type: ignore
                connect_user(self.utilisateur_cible.id)       #type: ignore
            
            all_notes = user_online[self.utilisateur_cible.id][0].lastNotes()       #type: ignore
            if (len(all_notes)//2) == 0:
                await interaction.user.send(f"{self.utilisateur_cible.display_name.capitalize()} n'a aucune nouvelle note.")        #type: ignore
                return
            elif (len(all_notes)//2) == 1:
                embed = discord.Embed(title=f"La Dernière Note De {self.utilisateur_cible.display_name.capitalize()}", description=f"La dernière note visible de <@{self.utilisateur_cible.id}> sur la page d'accueil de Pronote.", color=0x1365FF, url="")        #type: ignore
            else:
                embed = discord.Embed(title=f"Les {(len(all_notes))//2} Dernières Notes De {self.utilisateur_cible.display_name.capitalize()}", description=f"Les dernières notes visibles sur la page d'accueil de Pronote de <@{self.utilisateur_cible.id}>.", color=0x1365FF, url="")      #type: ignore

            for i in range(len(all_notes)):
                if i%2==0:
                    embed.add_field(name=all_notes[i], value=all_notes[i+1]+"\n──────────────", inline=False)


            await interaction.user.send(embed=embed)      #type: ignore
                
        async def moyenneGeneraleToSend_callback(interactionCallback: discord.Interaction):
            await interactionCallback.response.defer()
            await interactionCallback.message.delete()      #type: ignore
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:      #type: ignore
                await interactionCallback.channel.delete()      #type: ignore

            await interaction.user.send(f"**Ta demande a bien été accepté par {self.utilisateur_cible.mention} ! Tu recevras ce que tu as demandé dans quelques secondes...**")      #type: ignore

            if not verification_online_user(self.utilisateur_cible.id):       #type: ignore
                connect_user(self.utilisateur_cible.id)       #type: ignore
            
        
            moyenne = user_online[self.utilisateur_cible.id][0].getMoyenneGenerale()       #type: ignore


            embed = discord.Embed(title=f"La Moyenne Générale De {self.utilisateur_cible.display_name.capitalize()}", description=f"La moyenne générale de <@{self.utilisateur_cible.id}>.", color=0x00FE23, url="")      #type: ignore
            myn_eleve = float(moyenne[0].split(":")[1][1:].replace(",", "."))
            myn_classe = float(moyenne[1].split(":")[1][1:].replace(",", "."))
            embed.add_field(name="Élève", value=myn_eleve, inline=True)
            embed.add_field(name="Classe", value=myn_classe, inline=True)

            if myn_eleve > myn_classe:
                embed.set_footer(text="Il est au dessus de la moyenne de classe !")
            elif myn_eleve < myn_classe:
                embed.set_footer(text="Il est en dessous de la moyenne de classe !")
            elif myn_eleve == myn_classe:
                embed.set_footer(text="Sa moyenne est égale à la moyenne de classe !")


            await interaction.user.send(embed=embed)      #type: ignore   

        async def allMoyennesToSend_callback(interactionCallback: discord.Interaction):
            await interactionCallback.response.defer()
            await interactionCallback.message.delete()      #type: ignore
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:      #type: ignore
                await interactionCallback.channel.delete()      #type: ignore

            await interaction.user.send(f"**Ta demande a bien été accepté par {self.utilisateur_cible.mention} ! Tu recevras ce que tu as demandé dans quelques secondes...**")      #type: ignore

            if not verification_online_user(self.utilisateur_cible.id):       #type: ignore
                connect_user(self.utilisateur_cible.id)       #type: ignore
            
            all_moyennes = user_online[self.utilisateur_cible.id][0].getAllMoyennes()       #type: ignore

            embed = discord.Embed(title=f"Toutes Les Moyennes De {self.utilisateur_cible.display_name.capitalize()}", description=f"Les moyennes de <@{self.utilisateur_cible.id}> dans toutes ses matières.", color=0xFFBF13, url="")      #type: ignore

            for moyenne in all_moyennes:
                embed.add_field(name=moyenne[0], value=moyenne[1]+ "\n──────────────", inline=False)

            await interaction.user.send(embed=embed)      #type: ignore


        async def cancelSend_callback(interactionCallback: discord.Interaction):
            await interactionCallback.response.send_message("La demande a été rejetée !", ephemeral=True)
            await interactionCallback.message.delete()      #type: ignore
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:      #type: ignore
                await interactionCallback.channel.delete()      #type: ignore
            await interaction.user.send(f"**Ta demande a été réfusé par {interactionCallback.user.mention} !**")      #type: ignore
                

        toSendButton = Button(label="Envoyer", style=ButtonStyle.blurple)
        cancelButton = Button(label="Refuser", style=ButtonStyle.danger)
        demande_text = ""
        if self.name_channel == "edt":
            toSendButton.callback = edtToSend_callback      #type: ignore
            demande_text = f"**UNE DEMANDE D'EMPLOI DU TEMPS DE {interaction.user.mention}**,\n{interaction.user.mention} aimerait obtenir ton emploi du temps, il lui sera envoyé en MP. Acceptes-tu {self.utilisateur_cible.mention}?"      #type: ignore

        elif self.name_channel == "allDevoirs":
            toSendButton.callback = allDevoirsToSend_callback      #type: ignore
            demande_text = f"**UNE DEMANDE DE TOUS VOS DEVOIRS DE {interaction.user.mention}**,\n{interaction.user.mention} aimerait obtenir tous tes devoirs, ils lui seront envoyés en MP. Acceptes-tu {self.utilisateur_cible.mention}?"      #type: ignore

        elif self.name_channel == "lastNotes":
            toSendButton.callback = lastNotesToSend_callback      #type: ignore
            demande_text = f"**UNE DEMANDE DE TES DERNIÈRES NOTES DE {interaction.user.mention}**,\n{interaction.user.mention} aimerait obtenir tes dernières notes, elles lui seront envoyées en MP. Acceptes-tu {self.utilisateur_cible.mention}?"      #type: ignore

        elif self.name_channel == "moyenneG":
            toSendButton.callback = moyenneGeneraleToSend_callback      #type: ignore
            demande_text = f"**UNE DEMANDE DE TA MOYENNE GÉNÉRALE DE {interaction.user.mention}**,\n{interaction.user.mention} aimerait obtenir ta moyenne générale, elle lui sera envoyée en MP. Acceptes-tu {self.utilisateur_cible.mention}?"      #type: ignore

        elif self.name_channel == "allMoyennes":
            toSendButton.callback = allMoyennesToSend_callback      #type: ignore
            demande_text = f"**UNE DEMANDE DE TOUTES TES MOYENNES DE {interaction.user.mention}**,\n{interaction.user.mention} aimerait obtenir toutes tes moyennes, elles lui seront envoyées en MP. Acceptes-tu {self.utilisateur_cible.mention}?"      #type: ignore

        cancelButton.callback = cancelSend_callback      #type: ignore

        demandeView = View(timeout=None)
        demandeView.add_item(toSendButton)
        demandeView.add_item(cancelButton)

        
        await ticket.send(demande_text, view=demandeView)      #type: ignore
        await bot.get_user(self.utilisateur_cible.id).send(f"Tu as une nouvelle demande de la part de {interaction.user.mention} dans le channel -> {ticket.mention}")      #type: ignore
        return


async def toSendAt_callback(interaction: discord.Interaction):
    if interaction.channel_id == 1035959724421681192: #TOUS LES BOUTONS CHANNEL
        myView = View(timeout=None)

        async def selectRequestMenu_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(requestsSomethingModal(channel_use=int(selectRequestMenu.values[0])))
            await interaction.delete_original_message()
            



        liste_option = [
            SelectOption(label="Emploi Du Temps", value="1031318493603303504"),
            SelectOption(label="Devoirs", value="1031318536448127136"),
            SelectOption(label="Dernières Notes", value="1031318616374779986"),
            SelectOption(label="Moyenne Générale", value="10359521093985280901111"),
            SelectOption(label="Toutes Vos Moyennes", value="10359521093985280902222")
        ]
        
        selectRequestMenu = Select(placeholder="Que souhaitez-vous demander ?", options=liste_option, max_values=1)
        selectRequestMenu.callback = selectRequestMenu_callback
        myView.add_item(selectRequestMenu)

        await interaction.response.send_message(view=myView, ephemeral=True)



    elif interaction.channel_id == 1035952109398528090: #MOYENNE CHANNEL
        myView = View(timeout=None)

        async def selectRequestMenu_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(requestsSomethingModal(channel_use=int(selectRequestMenu.values[0])))
            await interaction.delete_original_message()
            

        liste_option = [
            SelectOption(label="Moyenne Générale", value="10359521093985280901111"),
            SelectOption(label="Toutes Les Moyennes", value="10359521093985280902222")
        ]
        
        selectRequestMenu = Select(placeholder="Que souhaitez-vous demander ?", options=liste_option, max_values=1)
        selectRequestMenu.callback = selectRequestMenu_callback
        myView.add_item(selectRequestMenu)

        await interaction.response.send_message(view=myView, ephemeral=True)


    else: #LES AUTRES CHANNEL
        await interaction.response.send_modal(requestsSomethingModal(channel_use=interaction.channel_id))

# ===================================================================================================
# BOUTON, CHANNEL, EMBED, VIEWS PAR DEFAUT
# ===================================================================================================
if True:
    channel_dico = {
        "edt": 1031318493603303504,
        "prochains_devoirs": 1031318536448127136,
        "dernieres_notes": 1031318616374779986,
        "moyennes": 1035952109398528090,
        "all_buttons": 1035959724421681192,
        "register": 1036065317778112522,
        "suggestion": 1031199831915495464,
        "besoindaide": 1031321509039460454,
        "refresh": 1039611828285743226
    }


    
    edtButton = Button(label="Obtenir Votre Emploi Du Temps", style=ButtonStyle.blurple)
    allDevoirsButton = Button(label="Obtenir Tous Vos Devoirs", style=ButtonStyle.blurple)
    lastNotesButton = Button(label="Obtenir Toutes Vos Dernières Notes", style=ButtonStyle.blurple)
    moyenneGeneraleButton = Button(label="Obtenir Votre Moyenne Générale", style=ButtonStyle.blurple)
    allMoyennesButton = Button(label="Obtenir Toutes Vos Moyennes", style=ButtonStyle.blurple)
    connexionButton = Button(label="Se connecter", style=ButtonStyle.green)
    faireUneDemandeButton = Button(label="Demander à Un Utilisateur", style=ButtonStyle.green)
    refreshButton = Button(label="Actualiser la page", style=ButtonStyle.green)
    all_buttons = [edtButton, allDevoirsButton, lastNotesButton, moyenneGeneraleButton, allMoyennesButton,refreshButton, faireUneDemandeButton]

    registerButton = Button(label="S'enregistrer", style=ButtonStyle.green)
    suggestionButton = Button(label="Suggérer !", style=ButtonStyle.green)
    helpButton = Button(label="Contacter", style=ButtonStyle.danger)

    nextDayButton = Button(label="Jour Suivant", style=ButtonStyle.blurple)
    previousDayButton = Button(label="Jour Précédent", style=ButtonStyle.blurple)

        


    #Création des embeds
    embedEdt = discord.Embed(title=f"Votre Emploi Du Temps", description="Obtenez votre emploi du temps juste en cliquant sur le bouton ci-dessous.", color=0x947AFF, url="")
    embedAllDevoirs = discord.Embed(title=f"Tous Vos Devoirs", description="Obtenez tous vos prochains devoirs juste en cliquant sur le bouton ci-dessous.", color=0xFFE17A, url="")
    embedLastNotes = discord.Embed(title=f"Vos Dernières Notes", description="Obtenez vos dernières notes juste en cliquant sur le bouton ci-dessous.", color=0x7AFF8E, url="")
    embedMoyennes = discord.Embed(title=f"Vos Moyennes", description="Obtenez votre moyenne générale ou toutes vos moyennes juste en cliquant sur l'un des boutons ci-dessous.", color=0xFF7AFB, url="")
    embedAllButtons = discord.Embed(title=f"Toutes Les Actions", description="Intéragissez avec l'un des boutons ci-dessous pour obtenir ce que vous souhaitez.", color=0xA2FF7A, url="")
    embedRegister = discord.Embed(title=f"S'identifier", description=f"En cliquant sur ce bouton, un salon privé va être ouvert avec <@{1035021602838040576}> et uniquement vous et le bot auront accès à ce salon. Il vous indiquera comment vous connecter pour obtenir l'accès à tous les salons.", color=0x00FE23, url="")       #type: ignore
    embedSuggestion = discord.Embed(title=f"Une Idée ?", description=f"Vous avez une idée ou une suggestion qui pourrait améliorer le serveur ? Alors n'hésitez pas à me le faire part en cliquant sur le bouton ci-dessous !", color=0x00FE23, url="")       #type: ignore
    embedHelp = discord.Embed(title=f"Besoin D'Aide !", description=f"Si vous rencontrez le moindre soucis, n'hésitez pas à me contacter via le bouton ci-dessous afin de régler au plus vite votre problème et aider au développement du serveur.", color=0xFF0000, url="")
    embedRefresh = discord.Embed(title=f"Rafraîchir La Page", description="Si vous avez un problème avec les intéractions ou qu'il y a une mise à jour de vos données sur la page Pronote, cliquez sur le bouton ci-dessous pour actualiser la page.", color=0x00D8FF, url="")


    #Liaison des callbacks au bouton
    edtButton.callback = edtButton_callback
    allDevoirsButton.callback = allDevoirsButton_callback
    lastNotesButton.callback = lastNotesButton_callback
    moyenneGeneraleButton.callback = moyenneGeneraleButton_callback
    allMoyennesButton.callback = allMoyennesButton_callback
    registerButton.callback = registerButton_callback

    faireUneDemandeButton.callback = toSendAt_callback
    suggestionButton.callback = suggestionButton_callback
    helpButton.callback = helpButton_callback
    refreshButton.callback = refreshButton_callback

    nextDayButton.callback = nextDayEdtButton_callback
    previousDayButton.callback = previousDayEdtButton_callback




# ===================================================================================================
# EVENT
# ===================================================================================================

@bot.event
async def on_ready():
    
    for chann in channel_dico:
        await bot.get_channel(channel_dico[chann]).purge()   # type: ignore

    #Création des Views + Ajout des boutons
    edtView = View(timeout=None)
    allDevoirsView = View(timeout=None)
    lastNotesView = View(timeout=None)
    moyenneView = View(timeout=None)
    allButtonsView = View(timeout=None)
    registerView = View(timeout=None)
    suggestionView = View(timeout=None)
    helpView = View(timeout=None)
    refreshView = View(timeout=None)

    ########################################################
    edtView.add_item(edtButton) 
    allDevoirsView.add_item(allDevoirsButton)
    lastNotesView.add_item(lastNotesButton)
    moyenneView.add_item(moyenneGeneraleButton)
    moyenneView.add_item(allMoyennesButton)

    for i in [edtView,allDevoirsView,lastNotesView,moyenneView]:
        i.add_item(faireUneDemandeButton)


    registerView.add_item(registerButton)
    suggestionView.add_item(suggestionButton)
    helpView.add_item(helpButton)
    refreshView.add_item(refreshButton)

    for i in all_buttons:
        allButtonsView.add_item(i)
    
    

    #Envoyer dans les channels tous les embeds et boutons
    await bot.get_channel(channel_dico["edt"]).send(embed=embedEdt, view=edtView)       #type: ignore
    await bot.get_channel(channel_dico["prochains_devoirs"]).send(embed=embedAllDevoirs, view=allDevoirsView)       #type: ignore
    await bot.get_channel(channel_dico["dernieres_notes"]).send(embed=embedLastNotes, view=lastNotesView)       #type: ignore
    await bot.get_channel(channel_dico["moyennes"]).send(embed=embedMoyennes, view=moyenneView)       #type: ignore
    await bot.get_channel(channel_dico["all_buttons"]).send(embed=embedAllButtons, view=allButtonsView)       #type: ignore
    await bot.get_channel(channel_dico["register"]).send(embed=embedRegister, view=registerView)       #type: ignore
    await bot.get_channel(channel_dico["suggestion"]).send(embed=embedSuggestion, view=suggestionView)       #type: ignore
    await bot.get_channel(channel_dico["besoindaide"]).send(embed=embedHelp, view=helpView)       #type: ignore
    await bot.get_channel(channel_dico["refresh"]).send(embed=embedRefresh, view=refreshView)       #type: ignore

    status_server = True
    print("Le bot est prêt !")


@bot.event
async def on_member_join(member: discord.Member):
    arrivant_role = member.guild.get_role(1036037404345245756)
    await member.add_roles(arrivant_role)       #type: ignore


@bot.event
async def on_raw_typing(payload: discord.RawTypingEvent):
    if payload.channel_id not in [1036132553888899112, 1033896513467842611]: #Si ce n'est pas dans le channel "test-commands"
        return

    connect_user(payload.user_id)


# ===================================================================================================
# COMMANDES (!)
# ===================================================================================================


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
async def getEmploiDuTemps(ctx: commands.context.Context, utilisateur_cible=""):

    async def edtToSend_callback(interaction: discord.Interaction):
        if interaction.user.id != utilisateur_cible:       #type: ignore
            await interaction.response.send_message("Ce message ne te concerne pas !", ephemeral=True)
            return
        
        await interaction.response.defer()
        await ctx.author.send(f"**Ta demande a bien été accepté par {interaction.user.mention} ! Tu recevras ce que tu as demandé dans quelques secondes...**")      #type: ignore
        if not verification_online_user(interaction.user.id):       #type: ignore
            connect_user(interaction.user.id)       #type: ignore
            
        edt = user_online[interaction.user.id][0].getEmploiDuTemps()       #type: ignore
    
        embed = discord.Embed(title=f"Les cours de {interaction.user.display_name.capitalize()} pour : {edt[0]}", description=f"L'emploi du temps de <@{interaction.user.id}> pour : {edt[0]}", color=0x00FE23, url="")       #type: ignore

        for cours in edt[1]:
            cours[1] = "\n".join(cours[1]) + "\n--------------------"
            embed.add_field(name=cours[0], value=cours[1], inline=False)

        await interaction.message.delete()      #type: ignore
        await ctx.author.send(embed=embed)
        


    async def cancelSend_callback(interaction: discord.Interaction):
        if interaction.user.id == utilisateur_cible or interaction.user.id == ctx.author.id:       #type: ignore
            await interaction.response.send_message("La demande a été rejetée !", ephemeral=True)
            await interaction.message.delete()      #type: ignore
            await ctx.author.send(f"**Ta demande a été réfusé par {interaction.user.mention} !**")      #type: ignore
            
            
        else:
            await interaction.response.send_message("Ce message ne te concerne pas !", ephemeral=True)
            


    if utilisateur_cible.startswith("<@") and utilisateur_cible.endswith(">"):
        toSendButton = Button(label="Envoyer", style=ButtonStyle.blurple)
        cancelButton = Button(label="Refuser", style=ButtonStyle.danger)

        toSendButton.callback = edtToSend_callback
        cancelButton.callback = cancelSend_callback
        
        utilisateur_cible = int(utilisateur_cible[2:-1])
        demandeView = View(timeout=None)
        demandeView.add_item(toSendButton)
        demandeView.add_item(cancelButton)

        await ctx.message.delete()
        await ctx.send(f"**UNE DEMANDE D'EMPLOI DU TEMPS POUR <@{utilisateur_cible}>**,\nL'utilisateur {ctx.author.mention} aimerait obtenir ton emploi du temps, il lui sera envoyé en MP. Acceptes-tu ?", view=demandeView)
        await bot.get_user(utilisateur_cible).send(f"{ctx.author.mention} voudrait obtenir ton emploi du temps dans le channel -> {ctx.channel.mention}")      #type: ignore
        return

        

    edt = user_online[ctx.author.id][0].getEmploiDuTemps()
    
    embed = discord.Embed(title=f"Vos cours de : {edt[0]}", description=f"Votre emploi du temps de : {edt[0]}", color=0x00FE23, url="")

    for cours in edt[1]:
        cours[1] = "\n".join(cours[1]) + "\n--------------------"
        embed.add_field(name=cours[0], value=cours[1], inline=False)


    if str(utilisateur_cible).lower() == "dm":
        await ctx.author.send(embed=embed)
        await ctx.reply("Ton Emploi Du Temps t'as bien été envoyé en DM !")
        return

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
async def delete(ctx, number_of_messages):
    print([i.id for i in ctx.author.roles])
    if number_of_messages == "all" and 1031184414476087297 in [i.id for i in ctx.author.roles]:
        await ctx.channel.purge()

    elif number_of_messages.isdigit() and 1031184414476087297 in [i.id for i in ctx.author.roles]:
        number_of_messages = int(number_of_messages)
        messages = [ctx async for ctx in ctx.channel.history(limit=number_of_messages + 1)]

        for each_message in messages:
            await each_message.delete()


@bot.command(name="sendEmbed")
async def sendEmbed(ctx: commands.context.Context, fichier: str):
    listes_roles_id = [i.id for i in ctx.author.roles]       #type: ignore
    if 1031184414476087297 not in listes_roles_id:
        return
    
    if fichier == "nouveautes" and ctx.channel.id == 1037157529358180352:
        with open(f"toutesLesTxt/{fichier}.txt", "r", encoding="utf-8") as f:
            all_lignes = f.readlines()
            nouveautes = [all_lignes[0]]
            if all_lignes[0].split(" ")[-1][:-1] == "COMMANDE":
                all_lignes.pop(0)

                
                for ligne in all_lignes:
                    if ligne.startswith("!"):
                        nouveautes.append(ligne)

                    else:
                        if all_lignes[all_lignes.index(ligne)-1].startswith("!"):
                            nouveautes.append(ligne)
                        else:
                            nouveautes[-1] += ligne


            else:
                all_lignes.pop(0)

                for ligne in all_lignes:
                    if ligne.startswith("."):
                        nouveautes.append(ligne[1:])

                    else:
                        if all_lignes[all_lignes.index(ligne)-1].startswith("."):
                            nouveautes.append(ligne)
                        else:
                            nouveautes[-1] += ligne
                

        embed = discord.Embed(title=f"【 {nouveautes[0][:-1]} 】", color=0x00FE23, url="")
        nouveautes.pop(0)
        for i in range(len(nouveautes)):
            if i%2==0:
                embed.add_field(name=nouveautes[i], value=nouveautes[i+1], inline=False)

        await ctx.message.delete()
        await ctx.channel.send(embed=embed)


    if fichier == "reglement":
        with open(f"toutesLesTxt/{fichier}.txt", "r", encoding="utf-8") as f:
            all_lignes = f.readlines()
        embed = discord.Embed(title=f"__{all_lignes[0]}__",description=f"<@{1033898963352432680}> est présent pour s'assurer du respect des règles du serveur. S'il vous reprend à plusieurs reprises pour un non-respect des règles, vous risquez un Mute ou un Ban si c'est trop répétitif. En cas d'erreur du bot, rendez-vous dans le salon {bot.get_channel(1031321509039460454).mention} afin de décrire votre problème.", color=0x00FE23, url="")      #type: ignore
        all_lignes.pop(0)
        for i in range(len(all_lignes)):
            embed.add_field(name=f"*Règle n°{i+1}*", value=f"*{all_lignes[i][:-1]}*\n", inline=False)
        
        await ctx.message.delete()
        await ctx.channel.send(embed=embed)


@bot.command(name="sendNewCommands")
async def sendNewCommands(ctx: commands.context.Context):
    listes_roles_id = [i.id for i in ctx.author.roles]       #type: ignore
    if 1031184414476087297 not in listes_roles_id:
        return

    if ctx.channel.id == 1034657312062853201:
        await ctx.channel.purge()       #type: ignore
        with open(f"toutesLesTxt/toutes_les_commandes.txt", "r", encoding="utf-8") as f:
            all_lignes = f.readlines()
        embed = discord.Embed(title=f"__{all_lignes[0]}__", color=0x00FE23, url="")
        all_lignes.pop(0)
        for i in range(len(all_lignes)):
            embed.add_field(name=f"{all_lignes[i].split(':')[0]}", value=f"{all_lignes[i].split(':')[1]}", inline=False)
        

        await ctx.channel.send(embed=embed)


@bot.command(name="exit")
async def exit_program(ctx: commands.context.Context):
    if ctx.channel.id == 1035581533815308318 and 1031184414476087297 in [i.id for i in ctx.author.roles]:       #type: ignore
        sys.exit()


@bot.command(name="restart")
async def restart_connexion(ctx: commands.context.Context):
    if ctx.channel.id == 1035581533815308318 and 1031184414476087297 in [i.id for i in ctx.author.roles]:       #type: ignore
        await ctx.reply("Rédemarrage en cours...")
        print("redemarrage en cours")

        for channel in channel_dico:
            await bot.get_channel(channel_dico[channel]).send("Rédemarrage du serveur, merci de patienter...")       #type: ignore

        for discordId in user_online:
            if user_online[discordId][1] == True:
                user_online[discordId][0].close()
                user_online[discordId][1] = False

        for discordId in user_online:
            connect_user(discordId)

        await on_ready()

        await ctx.reply("Redémarrage terminé !")
        print("redemarrage terminé")



bot.run(os.getenv("TOKEN2"))