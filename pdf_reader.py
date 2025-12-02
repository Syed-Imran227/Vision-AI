import PyPDF2
import os

def read_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        return "File not found."
        
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
