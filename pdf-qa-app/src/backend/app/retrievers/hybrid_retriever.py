from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

def create_hybrid_retriever(chunks, vector_db):
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 5
    vector_retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,
            "fetch_k": 30
        }
    )

    hybrid_retriever = EnsembleRetriever(
        retrievers=[
            bm25_retriever,
            vector_retriever
        ],
        weights=[0.3, 0.7]
    )

    return hybrid_retriever