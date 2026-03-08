import pytesseract
import cv2
import numpy as np
from PIL import Image
import re

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_file):
    # Convert image to OpenCV format
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    # Thresholding (improves text visibility)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    return thresh


def extract_text(image_file):
    processed = preprocess_image(image_file)

    text = pytesseract.image_to_string(processed,config='--psm 6')

    return text


def extract_amount(text):
    # Detect numbers like 10,000 or 10000
    match = re.search(r'\d{1,3}(,\d{3})*|\d+', text)

    if match:
        amount = match.group()
        amount = amount.replace(",", "")
        return amount

    return None