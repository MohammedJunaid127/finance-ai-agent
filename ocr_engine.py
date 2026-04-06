import pytesseract
import easyocr
import cv2
import numpy as np
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)


def preprocess_image(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast (IMPORTANT)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=20)

    # Light blur
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    return gray


def extract_text_easyocr(image_file):
    image_file.seek(0)
    processed = preprocess_image(image_file)

    results = reader.readtext(processed)

    text = " ".join([res[1] for res in results])
    return text


def extract_text_tesseract(image_file):
    image_file.seek(0)
    processed = preprocess_image(image_file)

    text = pytesseract.image_to_string(
    processed,
    config='--psm 6 -c tessedit_char_whitelist=₹0123456789,'
)
    return text


def extract_text(image_file):
    image_file.seek(0)

    processed = preprocess_image(image_file)

    text = pytesseract.image_to_string(
        processed,
        config='--psm 6'
    )

    return text


def extract_amount(text):
    text = text.replace("\n", " ").replace("  ", " ")

    # 1️⃣ Prefer decimal amounts (e.g., 659.00)
    matches = re.findall(r'\b\d{2,6}\.\d{2}\b', text)
    for m in matches:
        amount = int(float(m))

        # ✅ Sanity filter
        if 10 <= amount <= 50000:
            return amount

    # 2️⃣ Handle ₹ misread as 7 (common OCR issue)
    text = text.replace("7", "₹", 1) if "₹" not in text else text

    match = re.search(r'₹\s?([\d,]{2,6})', text)
    if match:
        amount = int(match.group(1).replace(",", ""))

        # ✅ Sanity filter
        if 10 <= amount <= 50000:
            return amount

    # 3️⃣ Fallback: clean integer detection
    numbers = re.findall(r'\b\d{2,6}\b', text)

    numbers = [int(n) for n in numbers if 10 <= int(n) <= 50000]

    # Remove obvious transaction IDs (very large patterns)
    if numbers:
        return max(numbers)

    return None
def extract_merchant(text):
    text = text.replace("\n", " ")

    # Detect "Domino's Pizza"
    match = re.search(r"(Domino'?s\s*Pizza)", text, re.IGNORECASE)
    if match:
        return "Dominos"

    # General "to Merchant"
    match = re.search(r'to\s+([A-Za-z]+)', text, re.IGNORECASE)
    if match:
        return match.group(1)

    return "Unknown"

