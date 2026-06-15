import app.utils.rag_resources as rag_resources
from app.graph.workflow import graph


def process_chat(question, session_id):
    if rag_resources.retriever is None:
        return {
            "error": "Please upload a PDF first."
        }


    response = graph.invoke(
        {
            "question": question
        },
            config={
            "configurable": {
                "thread_id": session_id
        },
            "run_name": "pdf_qa_graph",
            "metadata": {
            "session_id": session_id
        }
        }
        
    )

    return {
        "answer": response["answer"],
        "source": response["route"],
        "sources": response["sources"]
    }