from app.graph.state import GraphState
import time
import app.utils.rag_resources as rag_resources

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