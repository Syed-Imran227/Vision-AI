from llm_client import LLMClient

llm = LLMClient()

def simple_summarize(text: str, max_sentences: int = 5) -> str:
    return llm.summarize_text(text)

def simple_answer_question(page_text: str, question: str) -> str:
    return llm.chat(f"Context: {page_text}\n\nQuestion: {question}")

def simplify_content(text: str) -> str:
    return llm.simplify_text(text)
