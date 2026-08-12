from core.llm_client import LLMClient
import sys

try:
    client = LLMClient()
    print("Testing connection to Gemini 2.0 Flash...")
    response = client.chat("Hello, are you online?")
    print(f"Response: {response}")
    if "trouble thinking" in response or "API key" in response:
        sys.exit(1)
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
