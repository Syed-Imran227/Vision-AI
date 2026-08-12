import json
from core.llm_client import LLMClient
from web.browser_control import get_accessibility_tree, interact_with_element, get_page_text_content, open_website, get_page_headings, get_page_links

class WebAgent:
    def __init__(self):
        self.llm = LLMClient()

    def navigate(self, user_goal: str):
        """
        Analyzes the current page and decides what to do to achieve the user_goal.
        Returns a tuple: (voice_feedback, action_result)
        """
        # 0. Check for direct scannability requests
        if "list headings" in user_goal.lower() or "read headings" in user_goal.lower():
            headings = get_page_headings()
            return f"Here are the headings:\n{headings}", "Listed headings."
            
        if "list links" in user_goal.lower() or "read links" in user_goal.lower():
            links = get_page_links()
            return f"Here are the main links:\n{links}", "Listed links."

        # 1. Get Page State
        dom_json = get_accessibility_tree()
        page_text = get_page_text_content()
        
        print(f"DEBUG: DOM Size: {len(dom_json)} chars")

        # 2. Ask LLM for Analysis & Action
        prompt = f"""
        You are an AI assistant for a BLIND user navigating a website.
        
        User Goal: "{user_goal}"
        
        Current Page Content (Summary):
        {page_text[:800]}...
        
        Interactive Elements (JSON):
        {dom_json[:15000]} 
        
        Task:
        1. Provide a "voice_summary" for the blind user. 
           - If the user wants to READ the page, extract and read the actual TEXT CONTENT from the page naturally, as a human would read it. Read headlines, key paragraphs, and important information in a flowing narrative style. Keep it concise but informative.
           - If it's a search result page, read the titles and descriptions of top results clearly.
           - If user wants to click a link, briefly confirm which link you're clicking.
           - IGNORE browser UI elements and focus ONLY on webpage content.
        
        2. Decide the next action. 
           - If the user wants to click a link or button, use "click" action. Match the link text flexibly (partial matches are OK).
           - If the page is blank or the user wants to go to a website, use "open".
           - If the user wants to type in a search box, use "type".
           - Otherwise, use "none".
        
        3. For clicking links:
           - Look for links whose text contains or closely matches the user's target
           - Be flexible with matching (e.g., "Gmail" can match "Sign in - Gmail")
           - Prioritize links with tag="a" (hyperlinks)
        
        Return JSON ONLY:
        {{
            "voice_summary": "...",
            "action": "click" | "type" | "open" | "none",
            "url": "https://..." (if action is open),
            "element_id": 123 (optional),
            "selector": "css_selector" (optional),
            "input_text": "..." (if typing)
        }}
        """
        
        try:
            response = self.llm.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            result_text = response.text.strip()
            print(f"DEBUG: LLM Response: {result_text[:200]}...")

            if result_text.startswith("```json"):
                result_text = result_text[7:-3]
            
            plan = json.loads(result_text)
            
            # 3. Execute Action
            feedback = plan.get("voice_summary", "")
            action = plan.get("action")
            eid = plan.get("element_id")
            selector = plan.get("selector")
            
            if action == "open":
                url = plan.get("url")
                if url:
                    open_website(url)
                    return feedback, f"Opened {url}"
                else:
                    return feedback, "No URL specified."

            elif action == "click":
                if interact_with_element(eid, "click", selector=selector):
                    return feedback, "Clicked element."
                else:
                    return feedback, "Failed to click."
            
            elif action == "type":
                text = plan.get("input_text", "")
                if interact_with_element(eid, "type", text, selector=selector):
                    # Often need to submit after typing search
                    interact_with_element(eid, "submit", selector=selector) 
                    return feedback, f"Typed {text} and submitted."
                else:
                    return feedback, "Failed to type."
            
            return feedback, "No action taken."
            
        except Exception as e:
            print(f"WebAgent Error: {e}")
            return "I'm having trouble understanding this page.", str(e)

    def open_and_navigate(self, url, goal):
        open_website(url)
        return self.navigate(goal)
