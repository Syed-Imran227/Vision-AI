# web_reader.py

from bs4 import BeautifulSoup

def extract_readable_text(html: str, max_chars: int = 2500) -> str:
    soup = BeautifulSoup(html, "html.parser")
    parts: list[str] = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text:
            parts.append(text)

    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)
        if text:
            parts.append(text)

    full_text = "\n".join(parts)
    return full_text[:max_chars]
