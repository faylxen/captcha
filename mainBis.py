# Import the required modules
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import image
import dataClients


if __name__ == "__main__":
    #driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    options = Options()
    options.add_argument("--disable-gpu")  # Désactive l'accélération matérielle
    options.add_argument("--no-sandbox") 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options = options)    
    driver.get("https://algeria.blsspainvisa.com/")
    time.sleep(2)  # Ajuster le délai si nécessaire

######################################"fermer la fenetre d'information"

    # Trouver l'élément avec la classe 'btn-close'
    try:
        btn_close = driver.find_element(By.CLASS_NAME, "btn-close")

        # Vérifier si l'élément est visible et cliquable
        if btn_close.is_displayed() and btn_close.is_enabled():
            # Cliquer sur l'élément
            btn_close.click()
            print("Le bouton 'btn-close' a été cliqué avec succès.")
        else:
            print("Le bouton 'btn-close' n'est pas visible ou cliquable.")
    except Exception as e:
        print(f"Erreur lors de la recherche ou du clic sur l'élément : {e}")


######################################## click sur book apointment
    time.sleep(2)
    # Attendre que les liens 'Book Appointment' soient visibles
    links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, "Book an "))
    )
    
    # Vérifier qu'il y a au moins deux liens
    if len(links) >= 2:
        # Initialiser l'ActionChains
        actions = ActionChains(driver)
        
        # Survoler le premier lien
        actions.move_to_element(links[0]).perform()
        print("Premier lien survolé avec succès.")

        # Attendre un court instant pour l'effet du survol
        time.sleep(2)
        
        # Cliquer sur le deuxième lien
        links[1].click()
        print("Deuxième lien cliqué avec succès.")
    else:
        print("Moins de deux liens 'Book Appointment' trouvés.")

    time.sleep(2)



    driver.save_screenshot("screenshot.png")
    x,y=image.find_and_click_text("screenshot.png","ALGERI")
    actions = ActionChains(driver)
    actions.move_by_offset(x, y).click().perform()
    print("Clic simulé à l'emplacement spécifié.")
        
    
    
    
    
    
    
    
    time.sleep(600)
    #for i in range (100000000):
        #time.sleep(3)
        #print("hola")





####pour plusieurs clients : sans oublie un vpn ou proxy sinon ils detectent l'address ip !
"""rom concurrent.futures import ThreadPoolExecutor
import dataClients

# Fonction pour traiter chaque client
def handle_client(client):
    try:
        options = Options()
        options.add_argument("--disable-gpu")  # Désactive l'accélération matérielle
        options.add_argument("--no-sandbox")  # Pour éviter les erreurs d'environnement
        options.add_argument("--headless")    # Exécute en mode headless (optionnel)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Accéder au site souhaité
        site_url = "https://example.com"  # Remplacez par l'URL de votre site
        driver.get(site_url)

        # Exemple : Remplir des champs avec les données du client
        # Remplacez les sélecteurs par ceux spécifiques à votre site
        driver.find_element("id", "firstName").send_keys(client["FirstName"])
        driver.find_element("id", "lastName").send_keys(client["LastName"])
        driver.find_element("id", "dob").send_keys(client["date-of-birth"])
        driver.find_element("id", "passportNumber").send_keys(client["passportNumber"])
        driver.find_element("id", "email").send_keys(client["Email"])
        driver.find_element("id", "submit").click()

        # Ajoutez des actions supplémentaires ici si nécessaire
        print(f"Client {client['FirstName']} traité avec succès.")

    except Exception as e:
        print(f"Erreur lors du traitement du client {client['FirstName']}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    clients = dataClients.clients

    # Utiliser ThreadPoolExecutor pour gérer plusieurs threads
    with ThreadPoolExecutor(max_workers=len(clients)) as executor:
        executor.map(handle_client, clients)

    print("Tous les clients ont été traités.")"""        