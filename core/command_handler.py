import time
import re
from system.system_control import *
from vision.screen_reader import read_screen_text
from vision.smart_screen_navigator import find_and_click
from vision.screen_describer import describe_screen
from core.llm_client import LLMClient

# Initialize LLM Client
llm = LLMClient()

# Global typing mode state
_typing_mode_active = False

def is_typing_mode():
    """Check if typing mode is currently active"""
    return _typing_mode_active

def set_typing_mode(active: bool):
    """Set typing mode state"""
    global _typing_mode_active
    _typing_mode_active = active


from audio.sound_engine import play_success, play_error

def process_command(cmd: str, ui_obj=None) -> str:
    cmd = cmd.lower().strip()
    
    # Special handling for typing mode
    # If in typing mode, check for stop command first
    if _typing_mode_active:
        if "stop typing" in cmd or "exit typing" in cmd or "end typing" in cmd:
            set_typing_mode(False)
            if ui_obj:
                ui_obj.set_status("Listening…")
            return "Typing mode disabled."
        else:
            # In typing mode, type everything said
            type_text(cmd)
            return ""  # No voice feedback during typing to avoid interruption
    
    # 1. Get Intent from LLM
    intent = llm.get_intent(cmd)
    action = intent.get("action", "chat")
    
    print(f"DEBUG: Intent={intent}")

    # Helper to hide UI
    def hide_ui():
        if ui_obj: ui_obj.minimize()
        time.sleep(0.2) # Wait for animation

    def show_ui():
        if ui_obj: ui_obj.restore()

    # 2. Execute Action
    if action == "click":
        hide_ui()
        target = intent.get("target", "")
        if find_and_click(target):
            show_ui()
            play_success()
            return f"Clicked {target}."
        show_ui()
        play_error()
        return f"I couldn't find '{target}' on the screen."

    elif action == "type":
        hide_ui()
        text = intent.get("text", "")
        type_text(text)
        show_ui()
        play_success()
        return f"Typing: {text}"
    
    elif action == "start_typing":
        set_typing_mode(True)
        if ui_obj:
            ui_obj.set_status("TYPING MODE - Say 'stop typing' to exit")
        return "Typing mode enabled. Everything you say will be typed. Say stop typing when done."

    elif action == "scroll":
        hide_ui()
        direction = intent.get("direction", "down")
        if direction == "up":
            scroll_up()
        else:
            scroll_down()
        show_ui()
        return f"Scrolling {direction}."

    elif action == "open_app":
        app = intent.get("app_name", "").lower()
        if "chrome" in app:
            open_chrome()
            return "Opening Chrome."
        elif "notepad" in app:
            open_notepad()
            return "Opening Notepad."
        elif "calculator" in app:
            open_calculator()
            return "Opening Calculator."
        else:
            return f"I don't know how to open {app} yet."

    elif action == "search":
        query = intent.get("query", "")
        from web.browser_control import is_browser_open
        
        if is_browser_open():
            # Context-aware: Search inside the current browser
            from web.web_agent import WebAgent
            agent = WebAgent()
            try:
                hide_ui()
                feedback, result = agent.navigate(f"search for {query}")
                show_ui()
                return f"{feedback} {result}"
            except Exception as e:
                show_ui()
                return f"Browser Error: {e}"
        else:
            # Default: System search (opens new tab/window)
            focus_url_bar()
            type_text(query)
            press_enter()
            return f"Searching for {query}"

    elif action == "describe_screen":
        hide_ui()
        result = describe_screen()
        show_ui()
        return result

    elif action == "summarize" or action == "simplify":
        hide_ui()
        # Use Visual Summarization as requested (OCR-like but smarter)
        from vision.screen_describer import summarize_screen
        summary = summarize_screen()
        
        show_ui()
        play_success()
        
        # Return summary for speech, but maybe keep UI clean?
        # The main loop sets UI to response. We can handle that there or here.
        return summary

    elif action == "read_pdf":
        path = intent.get("path", "")
        if not path:
            return "Please specify which PDF file to read."
        from vision.pdf_reader import read_pdf
        text = read_pdf(path)
        return f"Read {len(text)} characters from PDF. I can summarize it if you like."

    elif action == "browser_action":
        goal = intent.get("goal", "")
        from web.web_agent import WebAgent
        agent = WebAgent()
        try:
            hide_ui()
            feedback, result = agent.navigate(goal)
            show_ui()
            return f"{feedback} {result}"
        except Exception as e:
            show_ui()
            return f"Browser Error: {e}"

    elif action == "exit":
        # Clean up browser before exiting
        try:
            from web.browser_control import _driver
            if _driver is not None:
                _driver.quit()
        except Exception as e:
            print(f"Browser cleanup error: {e}")
        
        # Trigger shutdown
        import main
        main.request_shutdown()
        return "Shutting down. Goodbye!"

    elif action == "chat":
        return intent.get("response", "I didn't understand that.")

    elif action == "where_am_i":
        from system.system_control import get_active_window_title
        window_title = get_active_window_title()
        
        # If Chrome is active, get more details
        if "Chrome" in window_title or "Edge" in window_title:
            from web.browser_control import is_browser_open, get_page_title
            if is_browser_open():
                page_title = get_page_title()
                play_success()
                return f"You are in {window_title}, on the webpage: {page_title}"
        
        play_success()
        return f"You are currently in: {window_title}"

    elif action == "keyboard_action":
        k_type = intent.get("type", "")
        from system.system_control import switch_window, close_tab, go_back, copy_selection, paste_selection
        
        if k_type == "switch_window":
            switch_window()
            return "Switching window."
        elif k_type == "close_tab":
            close_tab()
            return "Closing tab."
        elif k_type == "go_back":
            go_back()
            return "Going back."
        elif k_type == "copy":
            copy_selection()
            return "Copied."
        elif k_type == "paste":
            paste_selection()
            return "Pasted."
        
        return "Unknown keyboard action."

    return "I'm not sure what to do."
