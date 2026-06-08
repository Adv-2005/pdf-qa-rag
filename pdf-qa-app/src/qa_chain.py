from langchain.chains import RetrievalQA
from langchain_ollama import ChatOllama

def build_chain(vector_db):

    retriever = vector_db.as_retriever()

    llm = ChatOllama(
    model="gemma4:e4b",
    temperature=0
)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return chain