from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#
#creer une variable pour déclencher le driver
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
driver.get(r"https://ent.iledefrance.fr/auth/login?callback=%2Fcas%2Flogin%3Fservice%3Dhttps%253A%252F%252F0911632E.index-education.net%252Fpronote%252Feleve.html#/")

time.sleep(3)
try:
    email_adresse = driver.find_element(By.ID, "email")
    email_adresse.send_keys("prenom.nom")

    password_location = driver.find_element(By.ID, "password")
    password_location.send_keys("????")

    driver.find_element(By.CLASS_NAME, "flex-magnet-bottom-right").click()
except:
    print("echec")

# driver.close()
# driver.quit()
# driver.find_element(By.XPATH, "//span[text()='Ajouter au panier']").click()
# driver.find_element(By.XPATH, "//span[text()='10-11a']").click()
# driver.find_element(By.XPATH, "//a[@title='Mon panier']").click()
