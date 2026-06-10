from langchain_ollama import ChatOllama
import src.rag_resources as rag_resources
from src.tools import web_search
from src.graph_state import GraphState
from typing import Literal
from pydantic import BaseModel
import time

class GradeDocuments(BaseModel):
    binary_score: Literal["yes", "no"]

answer_llm = ChatOllama(
    model="qwen2.5:3b"
)

grader_llm = ChatOllama(
    model="qwen2.5:3b"
)

structured_llm = grader_llm.with_structured_output(
    GradeDocuments
)

def retrieve_node(state: GraphState):
    start = time.time()

    print("\nRETRIEVE NODE")
    print(state["question"])

    question = state["question"]

    docs = rag_resources.retriever.invoke(question)

    sources = []

    for doc in docs:

        sources.append({
            "page": doc.metadata.get(
                "page",
                "Unknown"
            ),
            "content": doc.page_content[:80]
        })

    print(
        f"Retrieve took {time.time()-start:.2f}s"
    )

    return {
        "documents": docs,
        "sources": sources
    }

def grade_documents(state: GraphState):
    start = time.time()

    question = state["question"]

    docs = state["documents"]

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a retrieval grader.

Your job is to determine whether the retrieved
documents contain enough information to answer
the user's question.

Question:
{question}

Retrieved Context:
{context}

Return:
yes -> if the documents are relevant
no -> if the documents are not relevant
"""

    result = structured_llm.invoke(prompt)

    relevance = result.binary_score
    
    print("GRADE:", relevance)
    print(
        f"Grader took {time.time()-start:.2f}s"
    )
    return {
        "relevance": relevance
    }

def rag_node(state: GraphState):
    start = time.time()
    print("USING RAG")

    question = state["question"]

    context = "\n\n".join(
        [doc.page_content for doc in state["documents"]]
    )
    prompt = f"""Answer the question using the context.

Question:
{question}

Context:
{context}
"""
    result = answer_llm.invoke(prompt).content
    print(
        f"RAG took {time.time()-start:.2f}s"
    )

    return {
        "answer": result,
        "route": "pdf"
    }

def web_node(state: GraphState):
    start = time.time()
    print("Using WEB SEARCH")

    question = state["question"]

    search_results = web_search.invoke(
        {"query": question}
    )

    prompt = f"""
Answer the user's question using the web search results.

Question:
{question}

Search Results:
{search_results}

Provide a concise and helpful answer.
"""

    answer = answer_llm.invoke(prompt).content
    print(
        f"Web search took {time.time()-start:.2f}s"
    )

    return {
        "answer": answer,
        "route": "web"
    }
