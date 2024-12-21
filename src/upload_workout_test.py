import pytesseract
import os
import cv2

tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract', 'Tesseract-OCR', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd =  tesseract_path


from PIL import Image

img = Image.open("assets/media/random-workout.png")

text = pytesseract.image_to_string(img, lang="ita")

lines = text.split("\n")

workout = {}

for line in lines:
    if line != "":
        print(line)