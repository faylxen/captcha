from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
# Configurer le driver
options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Maximiser la fenêtre du navigateur
driver.maximize_window()

# Charger la page
driver.get('file:///Users/faycal/Downloads/site_spain_html/8_apres_validation_demail.htm')

# Trouver toutes les divs avec la classe 'box-label'
divs = driver.find_elements(By.CLASS_NAME, 'box-label')

# Identifier le div visible
visible_div = None

for div in divs:
    # Vérification plus approfondie de la visibilité
    # On vérifie si l'élément a une taille (offsetWidth > 0 et offsetHeight > 0) et est affiché
    if div.is_displayed() and div.size['width'] > 0 and div.size['height'] > 0:
        visible_div = div
        print('Div visible trouvé:', div.text)
        break  # On arrête dès qu'on trouve un div visible

if visible_div is None:
    print("Aucun div visible n'a été trouvé.")

# Fermer le navigateur

# Fermer le navigateur
driver.quit()