from langgraph.graph import StateGraph, END

from src.graph_state import GraphState
from langgraph.checkpoint.memory import MemorySaver

from src.graph_nodes import (
    retrieve_node,
    grade_documents,
    rag_node,
    web_node,
    answer_validation_node,
    fallback_node,
    rewrite_query_node
)
def route_question(state):

    return state["relevance"]

def route_answer(state):

    return state["answer_found"]

workflow = StateGraph(GraphState)

workflow.add_node(
    "rewrite",
    rewrite_query_node
)

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

workflow.add_node(
    "answer_validation",
    answer_validation_node
)

workflow.add_node(
    "fallback",
    fallback_node
)

workflow.set_entry_point("rewrite")


workflow.add_edge(
    "rewrite",
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
    "answer_validation"
)

workflow.add_edge(
    "web",
    "answer_validation"
)

workflow.add_conditional_edges(
    "answer_validation",
    route_answer,
    {
        "yes": END,
        "no": "fallback"
    }
)

workflow.add_edge(
    "fallback",
    END
)
memory = MemorySaver()


graph = workflow.compile(
    checkpointer=memory
)