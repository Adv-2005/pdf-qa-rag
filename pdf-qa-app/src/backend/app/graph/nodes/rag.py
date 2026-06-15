from app.graph.state import GraphState
import time
from app.llms.openai import answer_llm
from langchain_core.messages import HumanMessage, AIMessage

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