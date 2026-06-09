import streamlit as st
import os 
from src.loader import load_pdf 
from src.splitter import split_documents
from src.vector_store import create_vector_store
from src.qa_chain import build_chain
from src.embeddings import get_embeddings
from src.tools import set_retriever, pdf_search, set_qa_chain, rag_answer
from src.tools import web_search

UPLOAD_DIR = "data/uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

st.title("PDF Q&A App")
st.set_page_config(
    page_title="PDF Q&A App",
    page_icon="📄"
)

pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)
if pdf:

    file_path = os.path.join(
        UPLOAD_DIR,
        pdf.name
    )

    with open(file_path, "wb") as f:
        f.write(pdf.getbuffer())

    st.success("PDF uploaded successfully")
    with st.spinner("Processing PDF..."):

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
        st.session_state.qa_chain = qa_chain
        st.success(
        f"PDF processed successfully! "
        f"({len(docs)} pages, {len(chunks)} chunks)"
    )
question = st.text_input(
    "Ask a question"
)
if st.button("Test PDF Search Tool"):

    if question:

        result = pdf_search.invoke(
            {"query": question}
        )

        st.subheader("Retrieved Chunks")

        st.write(result)

if st.button("Test RAG Tool"):

    result = rag_answer.invoke(
        {"question": question}
    )

    st.subheader("RAG Tool Output")

    st.write(result)

if st.button("Test Web Search Tool"):

    result = web_search.invoke(
        {"query": question}
    )

    st.subheader("Web Search Results")

    st.write(result)