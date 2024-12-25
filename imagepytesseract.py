from PIL import Image
import pytesseract

# Charger l'image
image = Image.open('image.png')

# Extraire les données de l'image, y compris les positions du texte
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

# Afficher les résultats
for i in range(len(data['text'])):
    text = data['text'][i]
    if text.strip():  # Si le texte n'est pas vide
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        print(f"Texte: {text}")
        print(f"Position: x={x}, y={y}, largeur={w}, hauteur={h}")
