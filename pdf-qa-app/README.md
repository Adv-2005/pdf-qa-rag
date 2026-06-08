# PDF Q&A Application

A Retrieval Augmented Generation (RAG) application built with LangChain.

## Features

- PDF Upload
- Semantic Search
- Vector Embeddings
- FAISS Vector Store
- RetrievalQA Chain

## Tech Stack

- LangChain
- Streamlit
- FAISS
- HuggingFace Embeddings
- OpenAI

## Architecture

PDF
↓
PyPDFLoader
↓
Chunking
↓
Embeddings
↓
FAISS
↓
Retriever
↓
LLM
↓
Answer