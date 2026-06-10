# PDF Q&A Agentic RAG

An Agentic Retrieval-Augmented Generation (RAG) application built with LangChain, FastAPI, React, and Ollama.

This project was created as a hands-on learning journey to understand:

* RAG (Retrieval-Augmented Generation)
* Tool Calling
* Agents
* LangGraph
* Agentic AI Systems

Instead of learning concepts in isolation, the goal is to implement each component incrementally through real projects.

---

## Features

### PDF Question Answering

Upload a PDF and ask questions about its content.

```text
PDF
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
```

---

### PDF Search Tool

Retrieve raw chunks from the uploaded PDF.

Example:

```text
User:
Show me the text related to leave policy.

Tool:
pdf_search
```

Returns relevant passages directly from the document.

---

### RAG Answer Tool

Answers questions using retrieved context from the uploaded PDF.

Example:

```text
User:
What is the notice period?

Tool:
rag_answer
```

---

### Web Search Tool

Uses SERP API to search the web for external or current information.

Example:

```text
User:
Who is the current RBI Governor?

Tool:
web_search
```

---

### Tool Calling Agent

An agent automatically selects the most appropriate tool:

```text
User Question
↓
Agent
├── pdf_search
├── rag_answer
└── web_search
↓
Response
```

---

### Modern Frontend

Built using:

* React
* Vite
* TailwindCSS
* Axios

---

## Tech Stack

### Backend

* Python
* FastAPI
* LangChain
* Ollama

### Frontend

* React
* Vite
* TailwindCSS
* Axios

### LLM

```text
gemma4:e4b
```

### Embedding Model

```text
nomic-embed-text
```

### Vector Database

```text
FAISS
```

### Search Provider

```text
SERP API
```

---

## Architecture

```text
React Frontend
        │
        ▼
FastAPI Backend
        │
        ▼
Tool Calling Agent
        │
        ├──────────────┐
        ▼              ▼
   PDF Tools      Web Search
        │              │
        ▼              ▼
     FAISS          SERP API
        │
        ▼
     Ollama
```

---

## Project Structure

```text
pdf-qa-rag/
│
├── backend/
│   └── main.py
│
├── data/
│   └── uploaded_pdfs/
│
├── src/
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── qa_chain.py
│   ├── tools.py
│   └── agent.py
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js
    │   └── components/
```

---

## Installation

### Clone Repository

```bash
git clone <repo-url>
cd pdf-qa-rag
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### Install Ollama Models

Embedding Model:

```bash
ollama pull nomic-embed-text
```

LLM:

```bash
ollama pull gemma4:e4b
```

---

### Configure Environment Variables

Create:

```text
.env
```

Add:

```env
SERP_API_KEY=your_serp_api_key
```

---

## Running the Backend

Start FastAPI:

```bash
uvicorn backend.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

API Docs:

```text
http://localhost:8000/docs
```

---

## Running the Frontend

Navigate to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Current Learning Progress

Completed:

* PDF Loading
* Text Chunking
* Embeddings
* FAISS Vector Store
* Retriever
* RAG Pipeline
* PDF Search Tool
* Web Search Tool
* Tool Calling Agent
* FastAPI Backend
* React Frontend

---

## Next Milestones

### LangGraph Router

```text
START
↓
Router Node
├── PDF Route
└── Web Route
↓
Answer Node
↓
END
```

---

### Agentic RAG

* Query Routing
* Query Rewriting
* Multi-Step Retrieval
* Tool Chaining

---

### Self-Correcting RAG

* Retrieval Evaluation
* Hallucination Detection
* Retry Logic
* Corrective RAG (CRAG)

---

### Research Agent

Future goal:

```text
Question
↓
Planner
↓
Web Search
↓
PDF Search
↓
Summarization
↓
Final Report
```

---

## Learning Philosophy

This project is intentionally built incrementally:

```text
PDF Loader
↓
Chunking
↓
Embeddings
↓
FAISS
↓
Retriever
↓
RAG
↓
Tools
↓
Agents
↓
LangGraph
↓
Agentic Systems
```

The focus is understanding how modern AI applications are built internally rather than simply using pre-built frameworks.
