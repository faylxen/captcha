import time
import cv2
import numpy as np
import easyocr
import pyautogui

def find_and_click_text(image_path, target_text):
    # Start timing
    start_time = time.time()
    
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    
    # Read the image
    image = cv2.imread(image_path)
    
    # Perform text detection
    results = reader.readtext(image_path, detail=1)
    
    # Flag to track if text was found and clicked
    text_clicked = False
    
    # Iterate through detected text regions
    for detection in results:
        text = detection[1]  # Extracted text
        bbox = detection[0]  # Bounding box coordinates
        
        # Check if target text is in the detected text
        if target_text in text:
            # Convert bbox to numpy array of integers
            bbox = np.array(bbox, dtype=int)
            
            # Calculate center of the bounding box
            center_x = int(np.mean(bbox[:, 0]))
            center_y = int(np.mean(bbox[:, 1]))

            print(center_x,"  ")
            
            # Optional: Draw rectangle around found text
            cv2.polylines(image, [bbox], isClosed=True, color=(0, 255, 0), thickness=2)
            
            # Move mouse and click
            

            print(f"Clicked on text: {text}")
            text_clicked = True
            
            # Optional: Display the image with bounding box
            cv2.imshow('Detected Text', image)
            cv2.waitKey(1000)  # Show for 1 second
            cv2.destroyAllWindows()
    
    # End timing
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Check if text was found and clicked
    if not text_clicked:
        print(f"No text containing '{target_text}' was found.")
    
    print(f"Execution time: {execution_time:.4f} seconds")
    return center_x,center_y

# Usage
if __name__ == "__main__":
    # Delay to switch to the target window
    print("Prepare the target window (5 seconds)...")
    time.sleep(5)
    
    # Path to your image
    image_path = 'image.png'
    
    # Text to find and click
    target_text = '746'
    
    # Find and click the text
    find_and_click_text(image_path, target_text)