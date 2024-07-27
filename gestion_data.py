import random
import sqlite3
from faker import Faker



class Data:
    #
    def __init__(self, base_de_donnees: str = "database.db"):
        """Initialisation des données

        Args:
            base_de_donnees (str): la base de données au format .db
        """
        self.conn = sqlite3.connect(base_de_donnees)
        self.c = self.conn.cursor()




    def write_new_user(self, discordId: int, EntId: str, EntMdp: str):
        """Ecrire un nouvel utilisateur dans la database

        Args:
            discordId (int): Id discord de l'utilisateur
            EntId (str): Id ent de l'utilisateur
            EntMdp (str): mdp ent de l'utilisateur
        """
        d = {
            "discordId": discordId,
            "EntId": EntId,
            "EntMdp": EntMdp
        }
        if self.get_user_by_discordId(discordId) == False:
            self.c.execute("INSERT INTO users VALUES (:discordId, :EntId, :EntMdp)", d)
            self.conn.commit()
        else:
            self.change_EntId(discordId, EntId)
            self.change_EntMdp(discordId, EntMdp)



    def get_user_by_discordId(self, discordId: int):
        self.c.execute(f"SELECT * FROM users WHERE discordId='{discordId}'")
        fetchall = self.c.fetchall()
        if fetchall == []:
            return False
        elif len(fetchall) <= 1:
            return fetchall[0]
        return fetchall


    def get_user_by_entId(self, EntId: str):
        self.c.execute(f"SELECT * FROM users WHERE EntId='{EntId}'")
        fetchall = self.c.fetchall()
        if fetchall == []:
            return False
        elif len(fetchall) <= 1:
            return fetchall[0]
        return fetchall


    def remove_user(self, discordId: int):
        """Supprimer l'utilisateur de la database

        Args:
            discordId (int): Id discord de l'utilisateur
        """
        self.c.execute(f"DELETE FROM users WHERE discordId='{discordId}'")
        self.conn.commit()

    def get_EntId(self, discordId: int):
        return self.get_user_by_discordId(discordId)[1]      #type: ignore


    def get_EntMdp(self, discordId: int):
        return self.get_user_by_discordId(discordId)[2]      #type: ignore


    def change_EntId(self, discordId: int, newEntId: str):
        """Change l'Id Ent de l'utilisateur discord

        Args:
            discordId (int): Id discord de l'utilisateur
            newEntId (str): Nouvel identifiant ENT lié à l'utilisateur discord
        """
        self.c.execute(f"UPDATE users SET EntId='{newEntId}' WHERE discordId='{discordId}'")
        self.conn.commit()


    def change_EntMdp(self, discordId: int, newMdpEnt: str):
        """Change le Mdp ENT de l'utilisateur discord

        Args:
            discordId (int): Id discord de l'utilisateur
            newMdpEnt (str): Nouvel mot de passe ENT lié à l'utilisateur discord
        """
        self.c.execute(f"UPDATE users SET EntMdp='{newMdpEnt}' WHERE discordId='{discordId}'")
        self.conn.commit()









def new_random_users():
    discordIdRandom = random.randint(10**17, 9*10**17)
    fake = Faker(locale="fr_FR")
    EntIdRandom = f"{fake.first_name().lower()}.{fake.last_name().lower()}"
    EntMdpRandom = f"{fake.password()}"

    donnees.write_new_user(discordIdRandom, EntIdRandom, EntMdpRandom)


if __name__ == "__main__":

    donnees = Data("database.db")

    #Creer un utilisateur aléatoire
    # new_random_users()

    #Supprimer x utilisateurs
    # x = 342844770469316910
    # donnees.remove_user(x)

    #changer l'id ent de y utilisateurs
    y = 203272768844857353


    #recuperer les utilisateurs
    # print(donnees.get_all_users())
