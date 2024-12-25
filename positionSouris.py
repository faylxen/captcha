from pynput.mouse import Controller
from pynput.keyboard import Listener, Key
import threading

mouse = Controller()
show_position = False  # Variable pour contrôler l'affichage


def track_mouse():
    """Affiche la position de la souris si la variable show_position est activée."""
    global show_position
    try:
        while True:
            if show_position:
                position = mouse.position
                print(f"Position actuelle de la souris : x={position[0]}, y={position[1]}")
                show_position = False  # Réinitialise après affichage
    except KeyboardInterrupt:
        print("Programme arrêté.")


def on_press(key):
    """Active l'affichage si la touche Entrée est pressée."""
    global show_position
    if key == Key.enter:
        show_position = True


# Lancer le suivi de la souris dans un thread séparé
mouse_thread = threading.Thread(target=track_mouse, daemon=True)
mouse_thread.start()

# Écouter les événements clavier globalement
with Listener(on_press=on_press) as listener:
    listener.join()
