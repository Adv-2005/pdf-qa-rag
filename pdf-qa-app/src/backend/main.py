from pathlib import Path
import traceback

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.tools import (
    set_retriever,
    set_qa_chain,
)
from src.loader import load_pdf
from src.splitter import split_documents
from src.vector_store import create_vector_store
from src.embeddings import get_embeddings
from src.qa_chain import build_chain
from src.agent import build_agent
import src.rag_resources as rag_resources
from src.graph import graph

app = FastAPI()
agent = None
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploaded_pdfs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global agent
    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Load PDF
        docs = load_pdf(str(file_path))
        # Split into chunks
        chunks = split_documents(docs)
        # Embeddings
        embeddings = get_embeddings()
        # Vector Store
        vector_db = create_vector_store(chunks, embeddings)
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})

        set_retriever(retriever)
        qa_chain = build_chain(vector_db)
        set_qa_chain(qa_chain)
        agent = build_agent()
        rag_resources.retriever = retriever
        rag_resources.qa_chain = qa_chain

        return {"message": "PDF uploaded successfully"}
    except ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Ollama is not running or is not reachable. "
                "Start Ollama, make sure the model is available, then retry the upload."
            ),
        ) from exc
    except Exception as exc:
        print("UPLOAD ERROR:")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(exc),
                "type": exc.__class__.__name__,
            },
        ) from exc

@app.post("/chat")
async def chat(data: dict):
    if rag_resources.retriever is None:
        return {
            "error": "Please upload a PDF first."
        }

    question = data["question"]

    response = graph.invoke(
        {
            "question": question
        }
    )

    return {
        "answer": response["answer"],
        "source": response["route"],
        "sources": response["sources"]
    }