from langchain_ollama import ChatOllama
import src.rag_resources as rag_resources
from src.tools import web_search
from src.graph_state import GraphState

llm = ChatOllama(
    model="gemma4:e4b"
)

def retrieve_node(state: GraphState):

    print("\nRETRIEVE NODE")
    print(state["question"])

    question = state["question"]

    docs = rag_resources.retriever.invoke(question)

    print(f"Retrieved {len(docs)} docs")

    return {
        "documents": docs
    }

def grade_documents(state: GraphState):

    question = state["question"]

    docs = state["documents"]

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a retrieval grader.

Question:
{question}

Retrieved Context:
{context}

Determine whether the retrieved context contains
enough information to answer the question.

Respond with only:

yes

or

no
"""

    result = llm.invoke(prompt)

    relevance = result.content.strip().lower()

    if "yes" in relevance:
        relevance = "yes"
    else:
        relevance = "no"
    
    print("GRADE:", relevance)
    return {
        "relevance": relevance
    }

def rag_node(state: GraphState):
    print("USING RAG")

    question = state["question"]

    result = rag_resources.qa_chain.invoke(
        {"input": question}
    )

    return {
        "answer": result["answer"]
    }

def web_node(state):
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

    answer = llm.invoke(prompt).content

    return {
        "answer": answer
    }
