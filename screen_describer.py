import pytesseract
import pyautogui
import cv2
import numpy as np
import os
from PIL import Image
from llm_client import LLMClient

# Initialize LLM
llm = LLMClient()

def describe_screen():
    # Take screenshot
    path = "nova_vision_temp.png"
    img = pyautogui.screenshot()
    img.save(path)
    
    # Try LLM Vision first
    try:
        description = llm.describe_image(path)
        if "API key" not in description:
            # Cleanup
            try: os.remove(path)
            except: pass
            return description
    except:
        pass

    # Fallback to OCR if LLM fails
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    data = pytesseract.image_to_data(img_cv, output_type=pytesseract.Output.DICT)

    screen_texts = []
    buttons = []

    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        conf = int(data['conf'][i]) if data['conf'][i].isdigit() else 0

        if conf > 50 and len(text) > 1:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            screen_texts.append(text)
            if h < 80 and w < 300:
                buttons.append(text)

    # Cleanup
    try: os.remove(path)
    except: pass

    desc = ""
    if len(screen_texts) == 0:
        return "I see a blank or non-textual screen, sir."

    desc += f"I see around {len(screen_texts)} text elements. "
    if len(buttons) > 0:
        btn_list = ", ".join(buttons[:8])
        desc += f"Buttons: {btn_list}. "

    sample = " ".join(screen_texts[:20])
    desc += f"Text: {sample}."

    return desc

def summarize_screen():
    # Take screenshot
    path = "nova_vision_summary.png"
    try:
        img = pyautogui.screenshot()
        img.save(path)
        
        # Use LLM Vision to summarize
        summary = llm.summarize_image(path)
        
        # Cleanup
        try: os.remove(path)
        except: pass
        
        return summary
    except Exception as e:
        print(f"Screen Summary Error: {e}")
        return "I couldn't summarize the screen."
