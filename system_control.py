# system_control.py

import os
import time
import pyautogui

pyautogui.FAILSAFE = False


def open_chrome():
    try:
        os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    except:
        os.system("start chrome")
    time.sleep(2)


def open_incognito():
    pyautogui.hotkey("ctrl", "shift", "n")
    time.sleep(1)


def open_notepad():
    os.system("start notepad")
    time.sleep(1)


def open_calculator():
    os.system("start calc")
    time.sleep(1)


def open_folder(name):
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.write(name)
    pyautogui.press("enter")


def type_text(text):
    pyautogui.write(text, interval=0.05)


def press_enter():
    pyautogui.press("enter")


def scroll_down():
    pyautogui.scroll(-800)


def scroll_up():
    pyautogui.scroll(800)


def focus_url_bar():
    pyautogui.hotkey("ctrl", "l")   # Focus URL bar
    time.sleep(0.2)


def extract_website(cmd):
    parts = cmd.split()
    for p in parts:
        if ".com" in p or ".in" in p or ".org" in p:
            return p
    return None
def get_active_window_title():
    """Get the title of the currently active window"""
    import ctypes
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value

def switch_window():
    import pyautogui
    pyautogui.hotkey('alt', 'tab')

def close_tab():
    import pyautogui
    pyautogui.hotkey('ctrl', 'w')

def go_back():
    import pyautogui
    pyautogui.hotkey('alt', 'left')

def copy_selection():
    import pyautogui
    pyautogui.hotkey('ctrl', 'c')

def paste_selection():
    import pyautogui
    pyautogui.hotkey('ctrl', 'v')
