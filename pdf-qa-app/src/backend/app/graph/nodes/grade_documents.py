from app.graph.state import GraphState
import time
from app.schemas.grader import GradeDocuments
from app.llms.openai import grader_llm

document_grader_structured_llm = grader_llm.with_structured_output(
    GradeDocuments
)

def grade_documents(state: GraphState):
    start = time.time()


    question = state["rewritten_question"]

    docs = state["documents"][:5]
    print("\n=== DOCUMENTS BEING GRADED ===\n")

    for i, doc in enumerate(state["documents"]):
        print(
        f"RANK {i+1}| PAGE: {doc.metadata.get('page')}"
    )
        print(doc.page_content[:300])
        print("\n-------------------\n")

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )
    print("\nQUESTION:")
    print(question)
    
    print("\nCONTEXT:")
    print(context)
    prompt = f"""
You are a retrieval grader.

Your task is to determine whether ANY part of the
retrieved context is relevant to answering the user's question.

The context does NOT need to contain the complete answer.

If at least one document contains information that would help answer the question,
return "yes".
Return "yes" if user explicitly asks for search in pdf or look for information in pdf etc.

Return "no" only if none of the retrieved context is relevant.
Return "no" if the user explicitly asks for web search,look on the internet, search online etc

Question:
{question}

Retrieved Context:
{context}

Return:
yes -> if the documents are relevant
no -> if the documents are not relevant
"""

    result = document_grader_structured_llm.invoke(prompt)

    relevance = result.binary_score
    
    print("GRADE:", relevance)
    print(
        f"Grader took {time.time()-start:.2f}s"
    )
    return {
        "relevance": relevance
    }