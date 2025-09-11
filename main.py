import cv2
import easyocr
from uteis import is_valid_plate 

reader = easyocr.Reader(['pt', 'en'])
img = cv2.imread('image.png')
results = reader.readtext(img)

valid_plates = []
texts = ["Brasil", "BR"]

for result in results:
    text = result[1]
    confidence = float(result[2])

    if len(text) < 6:
        continue

    if text.upper() in map(str.upper, texts):
        continue
    
    if is_valid_plate(text, confidence):
        valid_plates.append(text)

print("Placas válidas detectadas:", valid_plates)