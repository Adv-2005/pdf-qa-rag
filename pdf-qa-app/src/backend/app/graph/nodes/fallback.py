from app.graph.state import GraphState
def fallback_node(state: GraphState):

    return {
        "answer": (
            "Sorry, I could not find enough information "
            "to answer your question."
        )
    }