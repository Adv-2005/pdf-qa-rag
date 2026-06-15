from app.configs.settings import UPLOAD_DIR
from fastapi import UploadFile
from app.services.loader import load_pdf
from app.services.chunking import split_documents
from app.services.embeddings import get_embeddings
from app.services.vector_store import create_vector_store
from app.retrievers.hybrid_retriever import create_hybrid_retriever
from app.utils.tools import set_retriever
import app.utils.rag_resources as rag_resources


async def process_pdf(file: UploadFile ):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
            f.write(await file.read())
    docs = load_pdf(str(file_path))
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    vector_db = create_vector_store(
        chunks,
        embeddings
    )
    hybrid_retriever = (
        create_hybrid_retriever(
            chunks,
            vector_db
        )
    )

    set_retriever(hybrid_retriever)
    rag_resources.retriever = hybrid_retriever

    return {
    "filename": file.filename,
    "chunks": len(chunks)
}