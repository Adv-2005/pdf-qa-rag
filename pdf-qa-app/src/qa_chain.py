from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


def build_chain(vector_db):

    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question using only the provided context.

    Context:
    {context}

    Question:
    {input}

    Answer:
    """)

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 8}
    )

    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return retrieval_chain