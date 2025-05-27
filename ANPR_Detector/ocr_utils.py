# ocr_utils.py
# Tesseract OCR and image preprocessing

import cv2
import pytesseract
from config import TESSERACT_PATH

# OCR configuration
OCR_CONFIG = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def preprocess_plate_image(plate_img):
    """
    preprocess number plate image for better OCR accuracy

    - Convert to grayscale
    - Apply adaptive thresholding
    - Denoise
    - Enhance contrast using CLAHE
    """
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    denoised = cv2.fastNlMeansDenoising(binary)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    enhanced = clahe.apply(gray)

    return enhanced

def recognize_plate_number(plate_img):
    """
    run OCR on the cropped license plate image to extract plate number
    - applies preprocessing 
    - use tesseract OCR with strict alphanumeric whitelist
    - post-processing of text to filter out invalid results
    returns plate number string if valid, else none
    """
    try:
        processed_img = preprocess_plate_image(plate_img)
        plate_text = pytesseract.image_to_string(
            processed_img, config=OCR_CONFIG
        ).strip()

        plate_text = ''.join(c for c in plate_text if c.isalnum())
        if len(plate_text) >= 5:
            return plate_text
        else:
            return None
    except Exception as e:
        print(f"OCR Error: {str(e)}")

        return None
