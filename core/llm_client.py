from google import genai
from google.genai import types
import json
import os
from PIL import Image

class LLMClient:
    def __init__(self, config_path="config.json"):
        self.api_key = self._load_api_key(config_path)
        # Updated models list based on user request and new SDK
        self.models = ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash"]
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: No API key found. LLM features will be disabled.")

    def _load_api_key(self, config_path):
        key = os.getenv("GOOGLE_API_KEY")
        if key: return key
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return config.get("google_api_key")
        except:
            return None

    def _generate(self, prompt, image=None):
        if not self.client:
            raise Exception("No API key")

        last_error = None
        for model_name in self.models:
            try:
                if image:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=[prompt, image]
                    )
                else:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                return response.text
            except Exception as e:
                print(f"Warning: Model {model_name} failed ({e}). Switching to fallback...")
                last_error = e
                continue
        
        raise last_error or Exception("All models failed")

    def get_intent(self, user_text: str) -> dict:
        prompt = f"""
        You are the brain of an accessibility assistant named Vision AI.
        Analyze the user's command and map it to one of the following JSON actions:
        
        1. {{ "action": "click", "target": "text to click" }} -> If user wants to click something.
        2. {{ "action": "type", "text": "text to type" }} -> If user wants to type something once.
        3. {{ "action": "start_typing" }} -> If user wants to enter continuous typing mode (dictation mode).
        4. {{ "action": "scroll", "direction": "up/down" }} -> If user wants to scroll.
        5. {{ "action": "open_app", "app_name": "chrome/notepad/calculator" }} -> If user wants to open an app.
        6. {{ "action": "search", "query": "search query" }} -> If user wants to search the web.
        6. {{ "action": "search", "query": "search query" }} -> If user wants to search the web.
        7. {{ "action": "describe_screen" }} -> If user asks "describe this screen" or "what is this picture?" (Visual layout).
        8. {{ "action": "summarize" }} -> If user says "read the page", "summarize this", or "what does it say?" (Content summary).
        9. {{ "action": "simplify", "source": "screen/clipboard" }} -> If user wants simple explanation.
        10. {{ "action": "read_pdf", "path": "path/to/pdf" }} -> If user wants to read a PDF.
        11. {{ "action": "chat", "response": "your helpful response" }} -> For general questions.
        12. {{ "action": "browser_action", "goal": "user goal" }} -> If user wants to do something ON a website (click, search inside site, etc).
        13. {{ "action": "exit" }} -> If user says shutdown, exit, quit, or wants to stop.
        14. {{ "action": "where_am_i" }} -> If user asks "Where am I?", "What's in focus?", or "What app is this?".
        15. {{ "action": "keyboard_action", "type": "switch_window/close_tab/go_back/copy/paste" }} -> If user wants to use keyboard shortcuts.

        User Command: "{user_text}"
        
        Return ONLY the JSON object.
        """
        
        try:
            text = self._generate(prompt).strip()
            if text.startswith("```json"):
                text = text[7:-3]
            return json.loads(text)
        except Exception as e:
            print(f"LLM Error: {e}")
            return {"action": "chat", "response": "I'm having trouble connecting to my brain right now."}

    def chat(self, user_text: str) -> str:
        try:
            return self._generate(f"You are Vision AI, a helpful assistant. User says: {user_text}")
        except:
            return "I am having trouble thinking."

    def describe_image(self, image_path: str) -> str:
        try:
            img = Image.open(image_path)
            prompt = "Describe this screen in detail for a blind user. Mention the main content, any buttons, and the general layout. Be concise but descriptive."
            return self._generate(prompt, image=img)
        except Exception as e:
            print(f"Vision Error: {e}")
            return "I am having trouble seeing the screen right now."

    def summarize_image(self, image_path: str) -> str:
        try:
            img = Image.open(image_path)
            prompt = "Read the text on this screen and provide a concise summary (less than 50 words). Ignore UI elements, ads, and layout details. Focus ONLY on the main content."
            return self._generate(prompt, image=img)
        except Exception as e:
            print(f"Vision Summary Error: {e}")
            return "I couldn't read the screen."

    def summarize_text(self, text: str) -> str:
        try:
            return self._generate(f"Summarize the following text in less than 50 words. Focus ONLY on the main content and ignore menus/ads:\n\n{text}")
        except: return "Error summarizing text."

    def simplify_text(self, text: str) -> str:
        try:
            return self._generate(f"Explain the following text like I'm 5 years old. Keep it simple and clear:\n\n{text}")
        except: return "Error simplifying text."
