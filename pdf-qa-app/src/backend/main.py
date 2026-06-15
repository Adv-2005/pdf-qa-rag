# from pathlib import Path
# import traceback

from fastapi import FastAPI#, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from src.tools import (
#     set_retriever,
# )
# from src.loader import load_pdf
# from src.splitter import split_documents
# from src.vector_store import create_vector_store
# from src.embeddings import get_embeddings
# import src.rag_resources as rag_resources
# from src.graph import graph
# from langchain_community.retrievers import BM25Retriever
# from langchain.retrievers import EnsembleRetriever
from app.api.routes import router

app = FastAPI()
app.include_router(router)
# BASE_DIR = Path(__file__).resolve().parent.parent
# UPLOAD_DIR = BASE_DIR / "data" / "uploaded_pdfs"

# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):
#     global agent
#     file_path = UPLOAD_DIR / file.filename

#     try:
#         with open(file_path, "wb") as f:
#             f.write(await file.read())

#         # Load PDF
#         docs = load_pdf(str(file_path))
#         # Split into chunks
#         chunks = split_documents(docs)
#         # Embeddings
#         embeddings = get_embeddings()
#         # Vector Store
#         vector_db = create_vector_store(chunks, embeddings)
#         bm25_retriever = BM25Retriever.from_documents(chunks)
#         bm25_retriever.k = 5
#         vector_retriever = vector_db.as_retriever(
#     search_type="mmr",
#     search_kwargs={
#         "k": 10,
#         "fetch_k": 30
#     }
# )
    
#         hybrid_retriever = EnsembleRetriever(
#             retrievers=[
#                 bm25_retriever,
#                 vector_retriever
#             ],
#             weights=[0.3, 0.7]
#         )
#         set_retriever(hybrid_retriever)
#         rag_resources.retriever = hybrid_retriever

#         return {"message": "PDF uploaded successfully"}
#     except ConnectionError as exc:
#         raise HTTPException(
#             status_code=503,
#             detail=(
#                 "Ollama is not running or is not reachable. "
#                 "Start Ollama, make sure the model is available, then retry the upload."
#             ),
#         ) from exc
#     except Exception as exc:
#         print("UPLOAD ERROR:")
#         traceback.print_exc()
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "error": str(exc),
#                 "type": exc.__class__.__name__,
#             },
#         ) from exc

# @app.post("/chat")
# async def chat(data: dict):
#     session_id = data.get(
#     "session_id",
#     "default-session"
# )
#     if rag_resources.retriever is None:
#         return {
#             "error": "Please upload a PDF first."
#         }

#     question = data["question"]

#     response = graph.invoke(
#         {
#             "question": question
#         },
#             config={
#             "configurable": {
#                 "thread_id": session_id
#         },
#             "run_name": "pdf_qa_graph",
#             "metadata": {
#             "session_id": session_id
#         }
#         }
        
#     )

#     return {
#         "answer": response["answer"],
#         "source": response["route"],
#         "sources": response["sources"]
#     }