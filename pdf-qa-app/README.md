# PDF Q&A Agentic RAG

An Agentic Retrieval-Augmented Generation (RAG) application built using LangGraph, FastAPI, React, FAISS, BM25, OpenAI, and LangSmith.

The project evolved from a traditional Tool Calling Agent into a stateful LangGraph-based Agentic RAG system capable of:

* Hybrid Retrieval (BM25 + Vector Search)
* Query Rewriting
* Conversational Memory
* Document Relevance Grading
* Conditional Routing
* Web Search Fallback
* Hallucination Prevention
* Source Attribution
* LangSmith Observability

The goal of this project is to understand how production-grade AI systems are built internally rather than relying on black-box frameworks.

---

# Features

## PDF Question Answering

Upload a PDF and ask questions about its contents.

```text
PDF
↓
Chunking
↓
Embeddings
↓
FAISS
↓
Hybrid Retriever
↓
LangGraph Workflow
↓
Answer
```

---

## Hybrid Retrieval

The system combines:

```text
BM25 Keyword Search
+
MMR Vector Search
```

Implementation:

```python
EnsembleRetriever(
    retrievers=[
        bm25_retriever,
        vector_retriever
    ],
    weights=[0.5, 0.5]
)
```

Benefits:

* Better exact keyword matching
* Improved entity retrieval
* Stronger semantic search
* Better ranking quality

---

## Conversational Memory

Chat sessions maintain context across multiple turns.

Example:

```text
User:
What are the types of feedback?

Assistant:
Direct feedback
Indirect feedback

User:
Explain it
```

The system rewrites:

```text
Explain it
```

into:

```text
Can you explain the types of feedback?
```

before retrieval.

Memory is implemented using:

```python
MemorySaver
```

and session-based thread persistence.

---

## History-Aware Query Rewriting

Before retrieval, every question passes through a rewrite stage.

```text
Question
↓
Rewrite
↓
Retrieve
```

Purpose:

* Resolve references
* Improve retrieval quality
* Handle follow-up questions
* Improve ranking

Example:

```text
Who defined it?
```

↓

```text
Who defined machine learning?
```

---

## Agentic RAG Workflow

Current LangGraph architecture:

```text
Question
    │
    ▼
Query Rewriter
    │
    ▼
Hybrid Retrieval
    │
    ▼
Document Grader
 ┌──────┴──────┐
 │             │
 ▼             ▼
RAG       Web Search
 │             │
 └──────┬──────┘
        ▼
Answer Validation
 ┌──────┴──────┐
 │             │
 ▼             ▼
END       Fallback
```

---

## Document Relevance Grading

Retrieved documents are evaluated using an LLM.

Question:

```text
Does the retrieved context contain information
useful for answering the user's question?
```

Output:

```text
yes
or
no
```

This controls graph routing.

---

## Web Search Fallback

If relevant information is not found in the PDF:

```text
Question
↓
Retrieve
↓
Grade = No
↓
Web Search
↓
Answer
```

The system can therefore answer:

* PDF-specific questions
* General knowledge questions
* Missing-information queries

---

## Hallucination Prevention

The RAG node is instructed to return:

```text
INSUFFICIENT_INFORMATION
```

when the answer is not supported by context.

An answer validation stage checks generated responses.

Fallback:

```text
Sorry, I could not find enough information
to answer your question.
```

This reduces hallucinated answers.

---

## Source Attribution

Every response contains its source.

Example:

```text
📄 PDF
```

or

```text
🌐 Web
```

Backend Response:

```json
{
  "answer": "...",
  "source": "pdf"
}
```

---

## Retrieved Source Display

Retrieved chunks are displayed below responses.

Example:

```text
Sources

Page 13
Tom M. Mitchell's Definition...

Page 19
Spam Classification Example...
```

This improves transparency and debugging.

---

# Architecture

## LangGraph Workflow

```text
Question
↓
Rewrite Query
↓
Retrieve
↓
Grade Documents
├── Relevant
│   ↓
│   RAG
│
└── Not Relevant
    ↓
    Web Search

↓
Answer Validation
↓
Fallback (if needed)
```

---

# Project Structure
backend/
│
├── app/
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── graph/
│   │   ├── workflow.py
│   │   ├── state.py
│   │   │
│   │   ├── nodes/
│   │   │   ├── rewrite.py
│   │   │   ├── retrieve.py
│   │   │   ├── grade_documents.py
│   │   │   ├── rag.py
│   │   │   ├── web_search.py
│   │   │   ├── validate_answer.py
│   │   │   └── fallback.py
│   │   │
│   │   └── edges/
│   │       └── routing.py
│   │
│   ├── retrievers/
│   │   ├── vector_store.py
│   │   ├── hybrid_retriever.py
│   │   └── reranker.py
│   │
│   ├── llms/
│   │   ├── gemini.py
│   │   └── prompts.py
│   │
│   ├── schemas/
│   │   ├── requests.py
│   │   ├── grader.py
│   │   └── answer.py
│   │
│   ├── services/
│   │   ├── ingestion.py
│   │   ├── chat_service.py
│   │   ├── loader.py
│   │   ├── chunking.py
│   │   └── embeddings.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   └── utils/
│       ├── rag_resources.py
│       └── tools.py
│
├── data/
│   └── uploaded_pdfs/
│
├── tests/
│
├── main.py
│
├── requirements.txt
│
└── .env

# Installation

## Clone the Repository
* git clone https://github.com/Adv-2005/pdf-qa-rag.git
* cd backend

## Create Virtual Environment
* python -m venv venv
* venv\Scripts\activate

## Create Virtual Environment

### Windows
* python -m venv venv
* venv\Scripts\activate

### Linux/macOS
* python -m venv venv

* source venv/bin/activate

## Install Dependencies 
* pip install -r requirements.txt

## Configure Environment Variables
OPENAI_API_KEY=your_openai_api_key

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=pdf-qa-agentic-rag

## Start the Backend
* uvicorn main:app --reload
* Backend available at: http://localhost:8000

## Frontend Setup
* cd frontend
* npm install 
* npm run dev

* Frontend available at: http://localhost:5173

# Tech Stack

## Backend

* Python
* FastAPI
* LangChain
* LangGraph

## Frontend

* React
* Vite
* TailwindCSS
* Axios

## LLM

```text
gpt-4o-mini
```

## Embeddings

```text
text-embedding-3-small
```

## Retrieval

```text
FAISS
BM25
MMR
EnsembleRetriever
```

## Search Provider

```text
SERP API
```

## Observability

```text
LangSmith
```

---

# Current Capabilities

Completed:

* PDF Loading
* Text Chunking
* OpenAI Embeddings
* FAISS Vector Store
* BM25 Retrieval
* Hybrid Search
* MMR Search
* Query Rewriting
* Chat Memory
* History-Aware Retrieval
* LangGraph Migration
* Document Grading
* Conditional Routing
* Web Search Fallback
* Hallucination Prevention
* Answer Validation
* Source Attribution
* Source Display
* Structured Output Parsing
* LangSmith Tracing
* Retrieval Diagnostics
* Performance Benchmarking

---

# Current Challenges

* Document grader can be overly lenient when concepts are only mentioned briefly.
* Retrieval ranking can still occasionally bury the best chunk.
* Explicit web-search requests currently rely on prompt logic rather than a dedicated routing node.
* Answer grading requires further refinement.

---

