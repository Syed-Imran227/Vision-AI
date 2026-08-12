# utils.py

def is_website(cmd: str) -> bool:
    """Check if the command mentions a website domain."""
    website_keywords = [".com", ".in", ".org", ".edu", ".net", ".gov"]
    return any(ext in cmd for ext in website_keywords)


def extract_website(cmd: str) -> str | None:
    """Extract domain from a sentence like 'open google.com in chrome'."""
    tokens = cmd.split()
    for t in tokens:
        if any(ext in t for ext in [".com", ".in", ".org", ".edu", ".net", ".gov"]):
            return t
    return None
