
from PIL import Image
import pytesseract

# Path to the uploaded image
image_path = "/Users/faycal/Downloads/imagetest.png"

# Open the image file
image = Image.open(image_path)

# Use pytesseract to perform OCR on the image
extracted_text = pytesseract.image_to_string(image, config='--psm 6 digits')

print(extracted_text.strip())

