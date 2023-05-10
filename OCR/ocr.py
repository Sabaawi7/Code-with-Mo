import cv2
import numpy as np
import urllib.request
import pytesseract as ta

# Load the image from URL
url = input("Please input the image url: ")
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

# Preprocess the image
image = cv2.GaussianBlur(image, (5, 5), 0)

# Apply pytesseract to perform OCR
ta.pytesseract.tesseract_cmd = r"C:\Users\moham\AppData\Local\Tesseract-OCR\tesseract"
output = ta.image_to_string(image)
print(output)
