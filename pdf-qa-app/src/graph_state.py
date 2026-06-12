from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from typing import Annotated
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    question: str
    rewritten_question: str
    documents: List[Document]
    relevance: str
    route: str
    answer: str
    sources: list
    answer_found: str