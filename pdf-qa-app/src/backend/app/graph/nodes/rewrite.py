from app.graph.state import GraphState
from app.llms.openai import answer_llm

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
