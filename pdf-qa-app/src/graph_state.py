from typing import TypedDict, List
from langchain_core.documents import Document

class GraphState(TypedDict):
    question: str
    rewritten_question: str
    documents: List[Document]
    relevance: str
    route: str
    answer: str
    sources: list
    answer_found: str