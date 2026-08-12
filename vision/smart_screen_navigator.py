# smart_screen_navigator.py

import pytesseract
import pyautogui
import cv2
import numpy as np
import time
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def find_and_click(text_to_find: str):
    """
    Searches screen for given text and clicks it automatically.
    """

    # 1. Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 2. Run OCR with bounding boxes
    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    best_match = None
    best_conf = -1

    for i in range(len(data['text'])):
        word = data['text'][i].strip().lower()
        conf_val = data['conf'][i]
        if isinstance(conf_val, str):
            conf = int(conf_val) if conf_val.isdigit() else -1
        else:
            conf = int(conf_val)

        if conf < 40:
            continue

        # 3. Search for target text
        if text_to_find.lower() in word:
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            if conf > best_conf:
                best_conf = conf
                best_match = (x + w // 2, y + h // 2)

    # 4. If match found → Click
    if best_match:
        cx, cy = best_match
        pyautogui.moveTo(cx, cy, duration=0.2)
        pyautogui.click()
        return True

    return False
