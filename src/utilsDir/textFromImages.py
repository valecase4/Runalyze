import cv2
import pytesseract
import os

import pytesseract.pytesseract

tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract', 'Tesseract-OCR', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd =  tesseract_path

img_path = 'C://Users/Vale/Runalyze2/src/assets/media/random-workout.png'

def parse_content(file_path):
    workout = {

    }

    img = cv2.imread(file_path)

    date = img[50:200, 200:500]
    date = pytesseract.pytesseract.image_to_string(date)
    workout["Date"] = date

    main_stats = img[300:500, 0:img.shape[1]]
    main_stats = pytesseract.pytesseract.image_to_string(main_stats)
    workout["Main Stats"] = main_stats

    average_pace = img[500:650, 120:img.shape[1]]
    average_speed = img[650:780, 120:img.shape[1]]
    max_speed = img[780:930, 120:img.shape[1]]
    elevation_gain = img[930:1050, 120:img.shape[1]]
    elevation_loss = img[1050:1180, 120:img.shape[1]]
    start_time = img[1440:1580, 120:img.shape[1]]


    print(workout)

parse_content(img_path)