# ocr_reader.py

import os
import time
import pyautogui
import pytesseract
from PIL import Image

def read_screen_text() -> str:
    screenshot_path = os.path.join(os.getcwd(), "screen_temp.png")
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    time.sleep(0.3)

    text = pytesseract.image_to_string(Image.open(screenshot_path))

    try:
        os.remove(screenshot_path)
    except OSError:
        pass

    return text.strip()
