# config.py
# Configuration paths and Firebase setup

import os
import firebase_admin
from firebase_admin import credentials, db
import pytesseract

# Path to Tesseract.exe
TESSERACT_PATH = os.path.join(os.path.dirname(__file__), 'tesseract', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Firebase configuration
FIREBASE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'firebase_config.json')
FIREBASE_DB_URL = "https://smartparkingapp-1d951-default-rtdb.europe-west1.firebasedatabase.app/"

# initialise Firebase if not already initialised
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CONFIG_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })
