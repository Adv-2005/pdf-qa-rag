from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from langgraph.checkpoint.memory import MemorySaver
from app.graph.nodes.rewrite import rewrite_query_node
from app.graph.nodes.retrieve import retrieve_node
from app.graph.nodes.grade_documents import grade_documents
from app.graph.nodes.rag import rag_node
from app.graph.nodes.web_search import web_node
from app.graph.nodes.validate_answer import answer_validation_node
from app.graph.nodes.fallback import fallback_node

from app.graph.edges.routing import (
    route_question,
    route_answer
)


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