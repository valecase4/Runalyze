import cv2
import numpy as np
import pytesseract
import os

tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract', 'Tesseract-OCR', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd =  tesseract_path


img = cv2.imread('assets/media/random-workout.png')
print(img.shape)

date_section = img[50:200, 200:500]
main_stats_section = img[300:500, 0:img.shape[1]]
average_pace_section = img[500:650, 120:img.shape[1]]
average_speed_section = img[650:780, 120:img.shape[1]]
max_speed_section = img[780:930, 120:img.shape[1]]
elevation_gain_section = img[930:1050, 120:img.shape[1]]
elevation_loss_section = img[1050:1180, 120:img.shape[1]]
start_time_section = img[1440:1580, 120:img.shape[1]]

cv2.imshow("cropped", date_section)

text = pytesseract.image_to_string(average_pace_section, lang="ita")
print(text)

cv2.waitKey(0)
cv2.destroyAllWindows()