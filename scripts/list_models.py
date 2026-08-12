import google.generativeai as genai
import os
import json

def get_key():
    key = os.getenv("GOOGLE_API_KEY")
    if key: return key
    try:
        with open("config.json", "r") as f:
            return json.load(f).get("google_api_key")
    except: return None

key = get_key()
if not key:
    print("No API Key found")
else:
    genai.configure(api_key=key)
    print("Available Models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
