from gestion_data import *
from entClass import Ent
import random

status_ent = False
current_user_id = ""
user1 = ""

# 203272768844857353

while True:
    commande = input("Quel commande souhaitez-vous exécuter ? : ")

    if commande.startswith("!"):
        commande = commande[1:]

        if commande == "quit":
            break


        elif commande == "new_user":
            discordId = int(input("Entrez un identifiant (int) : "))           #random.randint(10**17, 9*10**17)
            EntId = input("Entrez votre identifiant ENT (prenom.nom) : ")
            EntMdp = input("Entrez votre mot de passe ENT : ")
            Data().write_new_user(discordId, EntId, EntMdp)


        elif commande == "remove_user":
            discordId = int(input("Quel est votre discord ID : "))
            Data().remove_user(discordId)


        elif commande == "changeMdp":
            discordId = int(input("Quel est votre discord ID : "))
            new_mdp = input("Votre nouveau mot de passe : ")
            Data().change_EntMdp(discordId, new_mdp)


        elif commande == "connexion" or (commande in ["getAllDevoirs", "lastNotes", "getMoyenne"] and status_ent == False):
            if status_ent == False:
                current_user_id = int(input("Quelle est votre discordId ? : "))
                current_user_id = 203272768844857353
                user1 = Ent()
                user1.connexion(current_user_id)
                
                status_ent = True
            else:
                print("Vous êtes déjà connecté !")

        if commande == "getAllDevoirs" and status_ent:
            print("-"*60)
            print(user1.getAllDevoirs())  # type: ignore

        elif commande == "lastNotes" and status_ent:
            print("-"*60)
            print(user1.lastNotes())  # type: ignore

        elif commande == "getMoyenne" and status_ent:
            print("-"*60)
            print(user1.getMoyenne())  # type: ignore