from code import interact
from glob import glob
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

        edt = user_online[interaction.user.id][0].getEmploiDuTemps()       #type: ignore
    
        embed = discord.Embed(title=f"Vos cours de : {edt[0]}", description=f"Votre emploi du temps de : {edt[0]}", color=0x00FE23, url="")

        for cours in edt[1]:
            cours[1] = "\n".join(cours[1]) + "\n--------------------"
            embed.add_field(name=cours[0], value=cours[1], inline=False)


        await interaction.response.send_message(embed=embed, ephemeral=True)




class requestsSomethingModal(discord.ui.Modal):
    def __init__(self, channel_use):
        self.channel_use = channel_use
        super().__init__(
            "Faire Une Demande"
        )
        self.username = discord.ui.TextInput(label="Faire une demande", min_length=2, max_length=124, required=True, placeholder="prenom.nom OU @pseudo(sans les #xxxx)", style=discord.TextInputStyle.short)

        if self.channel_use == 1031318493603303504:
            self.username.label = "Demander l'emploi du temps de"
                

        elif self.channel_use == 1031318536448127136:
            self.username.label = "Demander les prochains devoirs de"
            print("Prochain devoir")

        elif self.channel_use == 1031318616374779986:
            self.username.label = "Demander les dernières notes de"
            print("Derniere note")

        elif self.channel_use == 10359521093985280901111:
            self.username.label = "Demander la moyenne générale de"
            print("Vos moyennes G")

        elif self.channel_use == 10359521093985280902222:
            self.username.label = "Demander toutes les moyennes de"
            print("Vos moyennes all")

        elif self.channel_use == 1035959724421681192:
            self.username.label = "Demander l... de"
            print("Tous les boutons")

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
                    

                liste_option = [SelectOption(label=bot.get_user(membre_in_data[0]).display_name, value=f"{membre_in_data[0]}") for membre_in_data in self.utilisateur_data]
                selectUser = Select(placeholder="Plusieurs utilisateurs sont connectés à ce compte, à qui souhaitez-vous envoyer une demande ?", options=liste_option, max_values=1)
                selectUser.callback = selectUser_callback
                myView = View(timeout=None)
                myView.add_item(selectUser)
                await interaction.response.send_message(view=myView, ephemeral=True)
                return

        else:
            await interaction.response.send_message(f"L'utilisateur '{pseudo}' est introuvable", ephemeral=True)
            return

    async def create_ticket(self, interaction: discord.Interaction):
        ticket = discord.utils.get(bot.get_all_channels(), name=f"〘❔〙mes-demandes-{self.utilisateur_cible.name.lower()}-{self.utilisateur_cible.discriminator}")
        
        if ticket is not None:
            pass
        else:
            permission = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),       #type: ignore
                interaction.guild.get_member(self.utilisateur_cible.id): discord.PermissionOverwrite(view_channel = True, send_messages = False, read_message_history = True)       #type: ignore
            }

            ticket = await interaction.guild.create_text_channel(name=f"〘❔〙mes-demandes-{self.utilisateur_cible.name}-{self.utilisateur_cible.discriminator}", overwrites=permission)  # type: ignore



       
        await interaction.response.send_message(f"Votre demande a bien été envoyé à {self.utilisateur_cible.mention} !", ephemeral=True)

            
    
        async def edtToSend_callback(interactionCallback: discord.Interaction):
            
            await interactionCallback.response.defer()
            await interactionCallback.message.delete()
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:
                await interactionCallback.channel.delete()

            await interaction.user.send(f"**Ta demande a bien été accepté par {self.utilisateur_cible.mention} ! Tu recevras ce que tu as demandé dans quelques secondes...**")
            if not verification_online_user(self.utilisateur_cible.id):       #type: ignore
                connect_user(self.utilisateur_cible.id)       #type: ignore
                
            edt = user_online[self.utilisateur_cible.id][0].getEmploiDuTemps()       #type: ignore
        
            embed = discord.Embed(title=f"Les cours de {self.utilisateur_cible.display_name.capitalize()} pour : {edt[0]}", description=f"L'emploi du temps de <@{self.utilisateur_cible.id}> pour : {edt[0]}", color=0x00FE23, url="")       #type: ignore

            for cours in edt[1]:
                cours[1] = "\n".join(cours[1]) + "\n--------------------"
                embed.add_field(name=cours[0], value=cours[1], inline=False)


            await interaction.user.send(embed=embed)


        async def cancelSend_callback(interactionCallback: discord.Interaction):
            await interactionCallback.response.send_message("La demande a été rejetée !", ephemeral=True)
            await interactionCallback.message.delete()
            if len([msg async for msg in interactionCallback.channel.history()]) == 0:
                await interactionCallback.channel.delete()
            await interaction.user.send(f"**Ta demande a été réfusé par {interactionCallback.user.mention} !**")
                

        edtToSendButton = Button(label="Envoyer", style=ButtonStyle.blurple)
        cancelButton = Button(label="Refuser", style=ButtonStyle.danger)

        edtToSendButton.callback = edtToSend_callback
        cancelButton.callback = cancelSend_callback

        demandeView = View(timeout=None)
        demandeView.add_item(edtToSendButton)
        demandeView.add_item(cancelButton)

        
        await ticket.send(f"**UNE DEMANDE D'EMPLOI DU TEMPS DE {interaction.user.mention}**,\n{interaction.user.mention} aimerait obtenir ton emploi du temps, il lui sera envoyé en MP. Acceptes-tu {self.utilisateur_cible.mention}?", view=demandeView)
        await bot.get_user(self.utilisateur_cible.id).send(f"{interaction.user.mention} voudrait obtenir ton emploi du temps dans le channel -> {ticket.mention}")
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
            SelectOption(label="Toutes Vos Moyennes", value="10359521093985280902222")
        ]
        
        selectRequestMenu = Select(placeholder="Que souhaitez-vous demander ?", options=liste_option, max_values=1)
        selectRequestMenu.callback = selectRequestMenu_callback
        myView.add_item(selectRequestMenu)

        await interaction.response.send_message(view=myView, ephemeral=True)


    else: #LES AUTRES CHANNEL
        await interaction.response.send_modal(requestsSomethingModal(channel_use=interaction.channel_id))


channel_dico = {
        "test-channel": 1038862594401894440
    }

    
edtButton = Button(label="Obtenir Votre Emploi Du Temps", style=ButtonStyle.blurple)
faireUneDemandeButton = Button(label="Demander à Un Utilisateur", style=ButtonStyle.green)
embedEdt = discord.Embed(title=f"Votre Emploi Du Temps", description="Obtenez votre emploi du temps juste en cliquant sur le bouton ci-dessous.", color=0x00FE23, url="")
edtButton.callback = edtButton_callback
faireUneDemandeButton.callback = toSendAt_callback


@bot.event
async def on_ready():
    await bot.get_channel(channel_dico["test-channel"]).purge()
    edtView = View(timeout=None)
    edtView.add_item(edtButton) 
    edtView.add_item(faireUneDemandeButton)
    await bot.get_channel(channel_dico["test-channel"]).send(embed=embedEdt, view=edtView)       #type: ignore
    print("Le bot est prêt !")





bot.run(os.getenv("TOKEN3"))