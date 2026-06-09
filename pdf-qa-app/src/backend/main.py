from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.tools import (
    set_retriever,
    set_qa_chain
)
from src.loader import load_pdf
from src.splitter import split_documents
from src.vector_store import create_vector_store
from src.embeddings import get_embeddings
from src.qa_chain import build_chain
from src.agent import build_agent


app = FastAPI()
agent = None

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
    file_path = f"data/uploaded_pdfs/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Load PDF
    docs = load_pdf(file_path)
    # Split into chunks
    chunks = split_documents(docs)
    # Embeddings
    embeddings = get_embeddings()
    # Vector Store
    vector_db = create_vector_store(
        chunks,
        embeddings
    )
    retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)
    set_retriever(retriever)
    qa_chain = build_chain(vector_db)
    set_qa_chain(qa_chain)
    agent = build_agent()

    return {
        "message": "PDF uploaded successfully"
    }

@app.post("/chat")
async def chat(data: dict):
    if agent is None:
        return {
            "error": "Please upload a PDF first."
        }

    question = data["question"]

    response = agent.invoke(
        {
            "input": question
        }
    )

    return {
        "answer": response["output"]
    }