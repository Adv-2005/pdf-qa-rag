from langgraph.graph import StateGraph, END

from src.graph_state import GraphState

from src.graph_nodes import (
    retrieve_node,
    grade_documents,
    rag_node,
    web_node
)

def route_question(state):

    return state["relevance"]

workflow = StateGraph(GraphState)

workflow.add_node(
    "retrieve",
    retrieve_node
)

workflow.add_node(
    "grade",
    grade_documents
)

workflow.add_node(
    "rag",
    rag_node
)

workflow.add_node(
    "web",
    web_node
)

workflow.set_entry_point(
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "grade"
)

workflow.add_conditional_edges(
    "grade",
    route_question,
    {
        "yes": "rag",
        "no": "web"
    }
)

workflow.add_edge(
    "rag",
    END
)

workflow.add_edge(
    "web",
    END
)

graph = workflow.compile()