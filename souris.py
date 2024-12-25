import pyautogui
import time

# Désactiver le FAILSAFE si nécessaire
pyautogui.FAILSAFE = False

# Vérifiez la position actuelle pour ajuster vos coordonnées
print(f"Position actuelle de la souris : {pyautogui.position()}")

# Coordonnées des cases à cliquer
coordinates = [(1638, 176), (273, 1060), (1638, 1060)]

# Délai pour déplacer la souris sur la fenêtre correcte
time.sleep(5)  # Vous avez 5 secondes pour positionner la fenêtre

# Effectuer un clic sur chaque coordonnée
for x, y in coordinates:
    print(f"Déplacement vers ({x}, {y})")  # Log de débogage
    pyautogui.moveTo(x, y, duration=0.5)  # Déplacer la souris (0.5 sec pour atteindre la position)
    pyautogui.click()  # Cliquer
    time.sleep(1)  # Attendre une seconde entre les clics
