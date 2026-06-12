from langchain_openai import ChatOpenAI
import src.rag_resources as rag_resources
from src.tools import web_search
from src.graph_state import GraphState
from typing import Literal
from pydantic import BaseModel
import time
from langchain_core.messages import HumanMessage, AIMessage

class GradeDocuments(BaseModel):
    binary_score: Literal["yes", "no"]

class GradeAnswer(BaseModel):
    answer_found: Literal["yes", "no"]

answer_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

grader_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

document_grader_structured_llm = grader_llm.with_structured_output(
    GradeDocuments
)
answer_grader_structured_llm = grader_llm.with_structured_output(
    GradeAnswer
)

def rewrite_query_node(state: GraphState):
    print("\nSTATE KEYS")
    print(state.keys())
    messages = state.get("messages", [])

    question = state["question"]

    prompt = f"""
You are a query rewriting assistant.

Rewrite the latest user question so it can be
understood without the conversation history.

If the question is already clear and specific,
return it unchanged.

Only rewrite if it would improve retrieval.

Conversation History:
{messages}

Latest Question:
{question}

Rules:
- Preserve meaning.
- Use conversation context when needed.
- Resolve references like:
  "it", "that", "he", "they", "this concept".
- Return ONLY the rewritten query.
"""

    rewritten = answer_llm.invoke(prompt).content.strip()

    print("\nQUERY REWRITE")
    print("Original :", question)
    print("Rewritten:", rewritten)

    return {
        "rewritten_question": rewritten
    }

def retrieve_node(state: GraphState):
    start = time.time()

    print("\nRETRIEVE NODE")

    print("Original Query:")
    print(state["question"])

    print("\nRewritten Query:")
    
    print(state["rewritten_question"])
    print("\nTOP RETRIEVED CHUNKS:")

    question = state["rewritten_question"]
    docs = rag_resources.retriever.invoke(question)
    print("\nTOP RETRIEVED CHUNKS:")
    for i, doc in enumerate(docs[:3]):
        print(f"\nRank {i+1}")
        print(doc.page_content[:200])
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


    question = state["rewritten_question"]

    docs = state["documents"][:5]
    print("\n=== DOCUMENTS BEING GRADED ===\n")

    for i, doc in enumerate(state["documents"]):
        print(
        f"RANK {i+1}| PAGE: {doc.metadata.get('page')}"
    )
        print(doc.page_content[:300])
        print("\n-------------------\n")

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )
    print("\nQUESTION:")
    print(question)
    
    print("\nCONTEXT:")
    print(context)
    prompt = f"""
You are a retrieval grader.

Your task is to determine whether ANY part of the
retrieved context is relevant to answering the user's question.

The context does NOT need to contain the complete answer.

If at least one document contains information that would help answer the question,
return "yes".

Return "no" only if none of the retrieved context is relevant.

Question:
{question}

Retrieved Context:
{context}

Return:
yes -> if the documents are relevant
no -> if the documents are not relevant
"""

    result = document_grader_structured_llm.invoke(prompt)

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

    question = state["rewritten_question"]

    context = "\n\n".join(
        [doc.page_content for doc in state["documents"]]
    )
    prompt = f"""You are a question answering assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
respond exactly with:

INSUFFICIENT_INFORMATION


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
        "route": "pdf",
        "messages": [
        HumanMessage(content=question),
        AIMessage(content=result)
    ]
    }

def web_node(state: GraphState):
    start = time.time()
    print("Using WEB SEARCH")

    question = state["rewritten_question"]

    search_results = web_search.invoke(
        {"query": question}
    )

    prompt = f"""
Answer the user's question using ONLY the search results.

If the search results do not contain enough information
to answer the question, respond exactly with:

INSUFFICIENT_INFORMATION


Question:
{question}

Search Results:
{search_results}
"""

    answer = answer_llm.invoke(prompt).content
    print(
        f"Web search took {time.time()-start:.2f}s"
    )
    return {
        "answer": answer,
        "route": "web",
        "messages": [
        HumanMessage(content=question),
        AIMessage(content=answer)
    ]
}

def answer_validation_node(state: GraphState):

    answer = state["answer"]
    print("\n===== ANSWER VALIDATION =====")
    print(answer)
    print(state["answer"])
    if "INSUFFICIENT_INFORMATION" in answer:
        print("ROUTE -> FALLBACK")
        print("answer_found = no")
        return {
            "answer_found": "no"
        }
    print("ROUTE -> END")
    print("answer_found = yes")
    return {
        "answer_found": "yes"
    }

def fallback_node(state: GraphState):

    return {
        "answer": (
            "Sorry, I could not find enough information "
            "to answer your question."
        )
    }