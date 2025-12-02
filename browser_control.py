# browser_control.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

_driver = None

def get_driver() -> webdriver.Chrome:
    global _driver

    # Check if driver is actually alive
    if _driver is not None:
        try:
            _ = _driver.title
        except:
            try:
                _driver.quit()
            except:
                pass
            _driver = None

    if _driver is None:
        chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        if not os.path.exists(chrome_driver_path):
            raise FileNotFoundError("chromedriver.exe not found in project folder.")

        service = Service(chrome_driver_path)
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--guest") # Use Guest Mode as requested
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222") # Fix DevTools issues

        _driver = webdriver.Chrome(service=service, options=options)

    return _driver


def is_browser_open() -> bool:
    global _driver
    if _driver is None:
        return False
    try:
        # Check if we can get the title, implies window is open
        _ = _driver.title
        return True
    except:
        _driver = None # Reset if connection lost
        return False


def open_website(url: str):
    driver = get_driver()
    if not url.startswith("http"):
        url = "https://" + url
    driver.get(url)


def get_page_title() -> str:
    return get_driver().title


def get_accessibility_tree() -> str:
    """
    Returns a simplified JSON representation of the DOM, focusing on interactive elements.
    This is much lighter than full HTML for the LLM.
    """
    driver = get_driver()
    
    # JavaScript to extract useful elements
    script = """
    function getInteractiveElements() {
        const elements = document.querySelectorAll('a, button, input, textarea, select, [role="button"], [role="link"]');
        let data = [];
        
        elements.forEach((el, index) => {
            if (el.offsetParent === null) return; // Skip hidden elements
            
            let label = el.innerText || el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.value || "";
            label = label.replace(/\\s+/g, ' ').trim();
            
            if (label === "" && el.tagName.toLowerCase() === 'a') return; // Skip empty links
            
            // Generate a unique selector
            let selector = '';
            if (el.id) {
                selector = '#' + el.id;
            } else if (el.className && typeof el.className === 'string') {
                selector = '.' + el.className.split(' ').join('.');
            } else {
                selector = el.tagName.toLowerCase();
            }
            
            // Assign a temporary data-nova-id to the element to ensure we can click it
            el.setAttribute('data-nova-id', index);
            
            data.push({
                id: index,
                tag: el.tagName.toLowerCase(),
                text: label.substring(0, 50), // Limit text length
                type: el.getAttribute('type') || '',
                href: el.getAttribute('href') || ''
            });
        });
        return JSON.stringify(data);
    }
    return getInteractiveElements();
    """
    return driver.execute_script(script)


def interact_with_element(element_id: int = None, action: str = "click", text: str = "", selector: str = None):
    driver = get_driver()
    try:
        el = None
        if selector:
            # Try finding by direct CSS selector
            el = driver.find_element(By.CSS_SELECTOR, selector)
        elif element_id is not None:
            # Find by the custom attribute we injected
            el = driver.find_element(By.CSS_SELECTOR, f"[data-nova-id='{element_id}']")
        
        if not el:
            return False

        # Scroll into view to ensure we can interact
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", el)
        import time
        time.sleep(0.5) # Wait for scroll

        if action == "click":
            el.click()
        elif action == "type":
            el.click() # Focus the element first
            time.sleep(0.2)
            # Use pyautogui for "virtual keyboard" simulation as requested
            import pyautogui
            # Clear existing text first
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('backspace')
            time.sleep(0.1)
            pyautogui.write(text, interval=0.05) # Type like a human
        elif action == "submit":
            el.submit()
            
        return True
    except Exception as e:
        print(f"Interaction Error: {e}")
        return False


def get_page_text_content() -> str:
    """Returns the visible text of the main content for reading/summarization."""
    driver = get_driver()
    
    # JavaScript to extract main content intelligently
    script = """
    function extractMainContent() {
        // Helper to check if element is visible
        function isVisible(elem) {
            if (!elem) return false;
            const style = window.getComputedStyle(elem);
            return style.display !== 'none' && 
                   style.visibility !== 'hidden' && 
                   style.opacity !== '0' &&
                   elem.offsetWidth > 0 && 
                   elem.offsetHeight > 0;
        }

        // Helper to check if text is meaningful
        function isMeaningfulText(text) {
            return text.trim().length > 0 && 
                   !text.includes('{') && 
                   !text.includes('function(') && 
                   !text.includes('var ') &&
                   !text.includes('.css');
        }

        // 1. Remove clutter immediately
        const clutterSelectors = [
            'script', 'style', 'noscript', 'iframe', 'svg', 'path', 
            'nav', 'header', 'footer', 'aside', 
            '[role="navigation"]', '[role="banner"]', '[role="contentinfo"]',
            '.advertisement', '.ad', '.ads', '.cookie-banner', '.social-share',
            '#sidebar', '.sidebar', '.menu', '.nav'
        ];
        
        // Work on a clone to avoid modifying the actual page
        let root = document.body.cloneNode(true);
        
        clutterSelectors.forEach(selector => {
            root.querySelectorAll(selector).forEach(el => el.remove());
        });

        // 2. Use TreeWalker to extract text nodes
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    // Skip if parent is hidden
                    // Note: getComputedStyle doesn't work well on cloned nodes not in DOM
                    // So we rely on tag names and basic text checks here
                    const parentTag = node.parentElement.tagName.toLowerCase();
                    if (['script', 'style', 'noscript', 'svg', 'path'].includes(parentTag)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    if (!isMeaningfulText(node.textContent)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let result = [];
        let currentNode;
        
        while (currentNode = walker.nextNode()) {
            let text = currentNode.textContent.trim();
            // Basic heuristic to avoid CSS/JS code leaking through
            if (text.length > 1 && !text.startsWith('.') && !text.includes('{')) {
                result.push(text);
            }
        }
        
        // 3. Join with spaces and clean up
        let final = result.join(' ');
        final = final.replace(/\\s+/g, ' ').trim();
        
        return final.substring(0, 5000);
    }
    
    return extractMainContent();
    """
    
    try:
        return driver.execute_script(script)
    except Exception as e:
        print(f"Error extracting content: {e}")
        # Fallback to simple body text
        return driver.find_element(By.TAG_NAME, "body").text[:5000]

def get_page_headings() -> str:
    """Returns a list of headings on the page"""
    driver = get_driver()
    script = """
    function getHeadings() {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        let text = [];
        headings.forEach(h => {
            if (h.innerText.trim().length > 0 && h.offsetParent !== null) {
                text.push(h.tagName + ": " + h.innerText.trim());
            }
        });
        return text.join('\\n');
    }
    return getHeadings();
    """
    try:
        return driver.execute_script(script)
    except:
        return "No headings found."

def get_page_links() -> str:
    """Returns a list of main links on the page"""
    driver = get_driver()
    script = """
    function getLinks() {
        const links = document.querySelectorAll('a');
        let text = [];
        let seen = new Set();
        links.forEach(a => {
            let t = a.innerText.trim();
            if (t.length > 3 && a.offsetParent !== null && !seen.has(t)) {
                text.push("Link: " + t);
                seen.add(t);
            }
        });
        return text.slice(0, 20).join('\\n'); // Limit to top 20
    }
    return getLinks();
    """
    try:
        return driver.execute_script(script)
    except:
        return "No links found."
