# screen_reader.py

import pytesseract
import pyautogui
import os
import time
from PIL import Image


def read_screen_text():
    path = "nova_screen.png"
    img = pyautogui.screenshot()
    img.save(path)
    time.sleep(0.2)

    text = pytesseract.image_to_string(Image.open(path))

    try:
        os.remove(path)
    except:
        pass

    text = text.strip()
    return text if text else None
