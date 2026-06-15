from app.graph.state import GraphState
import time
from app.utils.tools import web_search
from app.llms.openai import answer_llm
from langchain_core.messages import HumanMessage, AIMessage

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
