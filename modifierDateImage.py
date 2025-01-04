import piexif
from PIL import Image
from datetime import datetime

def modifier_date_actuelle(image_path):
    """
    Modifie ou ajoute la date de prise de vue de l'image avec la date actuelle.
    
    Arguments :
    - image_path : Chemin de l'image à modifier.
    """
    
    # Obtenir la date actuelle au format requis
    nouvelle_date = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    
    # Charger l'image
    image = Image.open(image_path)
    
    try:
        # Charger les métadonnées EXIF existantes (s'il y en a)
        exif_dict = piexif.load(image.info.get("exif", b""))
    except FileNotFoundError:
        # Si aucune métadonnée n'existe, créer un dictionnaire vide
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "Interop": {}}
    
    # Ajouter ou modifier les champs liés à la date
    exif_dict["0th"][piexif.ImageIFD.DateTime] = nouvelle_date.encode("utf-8")
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = nouvelle_date.encode("utf-8")
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = nouvelle_date.encode("utf-8")
    
    # Appliquer les métadonnées modifiées
    exif_bytes = piexif.dump(exif_dict)
    image.save(image_path, exif=exif_bytes)
    
    print(f"Modification terminée. Nouvelle date : {nouvelle_date}")

# Exemple d'utilisation
modifier_date_actuelle("screenshot.png")
