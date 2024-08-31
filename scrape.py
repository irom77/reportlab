import pytesseract
from PIL import Image
import re
import os

# Specify the correct path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\irekr\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def read_numbers_from_image(image_path):
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file {image_path} does not exist.")

    # Open the image file
    image = Image.open(image_path)
    
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image)
    
    # Print the raw OCR output for debugging
    print("Raw OCR output:")
    print(text)
    
    # Use regex to find all numbers in the text
    numbers = re.findall(r'\d+', text)
    
    # Convert strings to integers
    numbers = [int(num) for num in numbers]
    
    return numbers

# Example usage
image_path = 'path_to_your_image.jpg'  # Replace this with your actual image path
try:
    # Print Tesseract version for debugging
    print("Tesseract version:")
    print(pytesseract.get_tesseract_version())
    
    extracted_numbers = read_numbers_from_image('images/red_siamese_cat_in_jungle.png')
    print(f"Numbers found in the image: {extracted_numbers}")
except FileNotFoundError as e:
    print(f"Error: {str(e)}")
except pytesseract.TesseractNotFoundError as e:
    print(f"Tesseract Error: {str(e)}")
    print("Please make sure Tesseract is correctly installed and the path is correct.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")