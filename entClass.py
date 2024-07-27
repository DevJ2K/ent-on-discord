"""La classe qui nous permettra de faire du scrapping sur l'ENT
"""


from gestion_data import Data
import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.webdriver.support import expected_conditions as EC
import time
import typer




logging.basicConfig(level=logging.INFO,
                    filename="all_log.log",
                    filemode="w",
                    encoding="utf_8",
                    format='entClass.py - %(asctime)s - %(levelname)s - %(message)s')


with open("adresse.json", "r") as f:
    liste_adresse = json.load(f)
    for i in liste_adresse:
        liste_adresse[i] = r"{}".format(liste_adresse[i])

    # print(liste_adresse)
    

class Ent:
    #Initialisation de la classe
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        
        self.options.add_argument('headless')
        self.options.add_argument("log-level=3")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        self.data = Data("database.db")
        self.adresse = r"https://ent.iledefrance.fr/auth/login?callback=%2Fcas%2Flogin%3Fservice%3Dhttps%253A%252F%252F0911632E.index-education.net%252Fpronote%252Feleve.html#/"
        
    #Attendre la présence d'un élément sur une page
    def waiting_page(self, tuple_id: tuple, wait_time = 10):
        try:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(tuple_id))
            return True
        except:
            print("Echec de l'accès à la page, veuillez réessayer plus tard...")
            
            # self.driver.close()
            return False
    
    #Se connecter à l'ENT
    def connexion(self, discordId):
        self.driver.get(self.adresse)
        
        try:
            
            self.waiting_page((By.ID, "email"))
            
            text =  typer.style(self.data.get_EntId(discordId), fg=typer.colors.BRIGHT_MAGENTA)

            logging.info(f"Connexion en tant que '{self.data.get_EntId(discordId)}' en cours...")
            typer.echo(f"Connexion en tant que '{text}' en cours...")

            email_adresse = self.driver.find_element(By.ID, "email")
            email_adresse.send_keys(self.data.get_EntId(discordId))

            password_location = self.driver.find_element(By.ID, "password")
            password_location.send_keys(self.data.get_EntMdp(discordId))

            self.driver.find_element(By.CLASS_NAME, "flex-magnet-bottom-right").click()
            

            if liste_adresse['pronote'] == self.adresse:
                if self.waiting_page((By.CLASS_NAME, "ibe_etab")):
                    logging.info(f"Connexion en tant que '{self.data.get_EntId(discordId)}' réussie !")
                    typer.echo(f"Connexion en tant que '{text}' réussie !")
                    return "successful"

                elif self.waiting_page((By.CLASS_NAME, "warning")):
                    return "mdp_incorrect"

            # elif liste_adresse['ent'] == self.adresse:
            #     print("TY1")
            #     if self.waiting_page((By.XPATH, "ode-portal[@name='Accueil'")):
            #         typer.echo(f"Connexion en tant que '{text}' réussie !")
            
        except:
            logging.error("Echec de l'acces à la page")
            self.driver.close()
            return "fail_server"

    # ====================================================================================================================
    # Méthode d'accès à des pages
    # ====================================================================================================================

    #Revenir sur la page d'accueil
    def _pageHome(self):
        self.waiting_page((By.ID, "GInterface.Instances[0].Instances[3]_Combo0"))
        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[3]_Combo0").click()
    
    def _pageNote(self):
        text = typer.style("notes", fg=typer.colors.BRIGHT_GREEN)
        logging.info(f"Accès à la page de vos 'notes' en cours...")
        typer.echo(f"Accès à la page de vos '{text}' en cours...")

        self.waiting_page((By.ID, "GInterface.Instances[0].Instances[1]_Combo2"))

        self.driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo2").click()

        typer.echo(f"Accès à la page de vos {text} réussie !")

        
    # ====================================================================================================================
    # Méthode pour la récupération de toutes les données
    # ====================================================================================================================

    #Récupérer l'intégralité des devoirs de la page principale
    def getAllDevoirs(self):
        text =  typer.style("devoirs", fg=typer.colors.BRIGHT_GREEN)
        logging.info(f"Récupération des 'devoirs' en cours...")
        typer.echo(f"Récupération des '{text}' en cours...")

        self.waiting_page((By.XPATH, "//div[@class='conteneur-liste-CDT']/ul/li[@role='listitem']"))

        all_homeworks = self.driver.find_elements(By.XPATH, "//div[@class='conteneur-liste-CDT']/ul/li[@role='listitem']")
        devoirs = [all_homeworks[all_homeworks.index(i)].text.split("\n") for i in all_homeworks]
        
        for journee in devoirs:
            while '' in journee:
                journee.remove('')
            while "J'ai terminé" in journee:
                journee.remove("J'ai terminé")

        logging.info(f"Vos prochains 'devoirs' ont bien été récupérés !")
        typer.echo(f"Vos prochains '{text}' ont bien été récupérés !")
        return devoirs

    #Récupérer l'intégralité des moyenne de la page note
    def getAllMoyennes(self):
        text =  typer.style("moyennes", fg=typer.colors.BRIGHT_GREEN)
        logging.info(f"Récupération de vos 'moyennes' en cours...")
        typer.echo(f"Récupération de vos '{text}' en cours...")

        self._pageNote()
        self.waiting_page((By.XPATH, "//div[@class='Gras Espace']"))

        get_all_notes = self.driver.find_elements(By.XPATH, "//div[@class='Gras Espace']")
        all_notes = []
        for note in get_all_notes:
            note = note.get_attribute("aria-label")
            all_notes.append(note.rsplit(" ", maxsplit=1))
            
        for i in all_notes:
            if i[1] == "":
                i[1] = "?"

        self._pageHome()
        logging.info(f"Vos 'moyennes' ont bien été récupérés !")
        typer.echo(f"Vos '{text}' ont bien été récupérés !")
        
        return all_notes



    # ====================================================================================================================
    # Méthode pour la récupération d'une donnée spécifique à partir d'un getAll_(self)
    # ====================================================================================================================


    #Dernières notes visibles sur la page principale
    def lastNotes(self):
        text =  typer.style("notes", fg=typer.colors.BRIGHT_GREEN)
        logging.info(f"Récupération des dernières 'notes' en cours...")
        typer.echo(f"Récupération des dernières '{text}' en cours...")

        self.waiting_page((By.XPATH, "//article[@class='widget theme-cat-resultat notes']"))

        get_all_last_notes = self.driver.find_elements(By.XPATH, "//article[@class='widget theme-cat-resultat notes']")
        last_notes = [get_all_last_notes[get_all_last_notes.index(i)].text.split("\n") for i in get_all_last_notes]

        last_notes = last_notes[0]
        last_notes.remove("Dernières notes")

        for date in last_notes[1::3]:
            last_notes.remove(date)

        logging.info(f"Vos {len(last_notes)//2} dernières 'notes' ont bien été récupérés !")
        typer.echo(f"Vos {len(last_notes)//2} dernières '{text}' ont bien été récupérés !")
        return last_notes
        

    def getDevoir(self, date: str):
        all_homeworks = self.getAllDevoirs()


    def getMenu(self):
        pass

    #Récupérer la moyenne de l'élève et de classe
    def getMoyenneGenerale(self):
        logging.info(f"Récupération de votre 'moyenne générale' en cours...")
        self._pageNote()
        self.waiting_page((By.ID, "GInterface.Instances[2].Instances[1]_piedDeListe"))
        moyenne = self.driver.find_elements(By.ID, "GInterface.Instances[2].Instances[1]_piedDeListe")
        moyenne = [i.text for i in moyenne]
        moyenne = moyenne[0].split("\n")
        self._pageHome()
        logging.info("Récupération de votre 'moyenne générale' réussie !")
        return moyenne

    def vieScolaire(self):
        pass

    def openENT(self):
        self.adresse = r"https://ent.iledefrance.fr/auth/login?callback=https%3A%2F%2Fent.iledefrance.fr%2Ftimeline%2Ftimeline#/"

    def getMsgENT(self):
        pass

    def reserverLaCantine(self):
        pass

    def getMoyenne(self):
        pass

    def getNote(self, matiere):
        pass

    def getEmploiDuTemps(self):

        text =  typer.style("emploi du temps", fg=typer.colors.BRIGHT_GREEN)
        logging.info(f"Récupération de votre 'emploi du temps' en cours...")
        typer.echo(f"Récupération de votre '{text}' en cours...")

    
        if self.waiting_page((By.CLASS_NAME, "container-heures"), wait_time=2) == False:
            return (False, self.driver.find_elements(By.CLASS_NAME, "as-date-picker")[0].text)


        prochain_heures = self.driver.find_elements(By.CLASS_NAME, "container-heures")
        prochain_cours = self.driver.find_elements(By.CLASS_NAME, "container-cours")

        liste_cours_recup = [i.text for i in prochain_cours]
        liste_cours_trier = [i.split("\n") for i in liste_cours_recup]

        liste_heures_recup = [i.text for i in prochain_heures]
        liste_heures_trier = [i.split("\n") for i in liste_heures_recup]

        heures_cours = [[h, c] for h, c in zip(liste_heures_trier, liste_cours_trier)]  # type: ignore
        heures_cours = [self.driver.find_elements(By.CLASS_NAME, "as-date-picker")[0].text ,heures_cours]

        logging.info(f"Votre 'emploi du temps' a été récupéré avec succès !")
        typer.echo(f"Votre '{text}' a été récupéré avec succès !")

        return heures_cours
        
    
    def nextDayEDT(self):
        text =  typer.style("emploi du temps", fg=typer.colors.BRIGHT_GREEN)
        logging.info(f"Récupération du jour suivant 'emploi du temps' en cours...")
        typer.echo(f"Récupération du jour suivant  '{text}' en cours...")

        edt_actuel = self.getEmploiDuTemps()

        self.waiting_page((By.XPATH, "//i[@class='icon_angle_right icon btnImageIcon btnImage OmbreFocus']"), wait_time=2)
        fleche_suivant = self.driver.find_element(By.XPATH, "//i[@class='icon_angle_right icon btnImageIcon btnImage OmbreFocus']")
        fleche_suivant.click()
        time.sleep(0.1)
        edt_suivant = self.getEmploiDuTemps()

        if edt_actuel == edt_suivant:
            return False
        return edt_suivant


    def previousDayEDT(self):
        text =  typer.style("emploi du temps", fg=typer.colors.BRIGHT_GREEN)
        logging.info(f"Récupération du jour précédent 'emploi du temps' en cours...")
        typer.echo(f"Récupération du jour précédent  '{text}' en cours...")

        edt_actuel = self.getEmploiDuTemps()

        self.waiting_page((By.XPATH, "//i[@class='icon_angle_left icon btnImageIcon btnImage OmbreFocus']"), wait_time=2)
        fleche_precedent = self.driver.find_element(By.XPATH, "//i[@class='icon_angle_left icon btnImageIcon btnImage OmbreFocus']")
        fleche_precedent.click()
        time.sleep(0.1)
        edt_precedent = self.getEmploiDuTemps()

        if edt_actuel == edt_precedent:
            return False
        return edt_precedent

    def close(self):
        self.driver.quit()
        del self


if __name__ == "__main__":
    user1 = Ent()
    user1.connexion(203272768844857353)
    print(user1.nextDayEDT())
    time.sleep(1)
    print(user1.previousDayEDT())
    
    