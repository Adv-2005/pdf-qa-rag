# PDF Q&A Agentic RAG

An Agentic Retrieval-Augmented Generation (RAG) application built using LangGraph, FastAPI, React, FAISS, and local/open-source LLMs.

The project evolved from a traditional Tool Calling Agent into a LangGraph-based Agentic RAG system capable of:

* Retrieval-Augmented Generation (RAG)
* Document Relevance Grading
* Conditional Routing
* Web Search Fallback
* Source Attribution
* Retrieval Evaluation

The goal of this project is to understand how modern AI systems are built internally rather than relying on black-box frameworks.

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
Retriever
↓
LangGraph Workflow
↓
Answer
```

---

## Agentic RAG Workflow

The system evaluates retrieved documents before generating an answer.

```text
Question
↓
Retrieve
↓
Document Grader
↓
Relevant?
├── Yes → RAG
└── No  → Web Search
↓
Answer
```

This enables:

* Better retrieval validation
* Dynamic routing
* Reduced hallucinations
* Improved answer quality

---

## Document Grading

Retrieved documents are evaluated using an LLM.

The grader determines:

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

This decision controls routing inside the graph.

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

This ensures the system can answer both PDF-specific and general knowledge questions.

---

## Source Attribution

Every response contains information about its source.

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
Retrieve Node
↓
Document Grader
↓
Relevant?
├── Yes
│   ↓
│   RAG Node
│
└── No
    ↓
    Web Search Node

↓
Final Answer
```

---

## Graph State

```python
{
    "question": str,
    "documents": list,
    "relevance": str,
    "answer": str,
    "route": str,
    "sources": list
}
```

---

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

## LLMs

Local:

```text
qwen2.5:3b
gemma4:e4b
```

Cloud:

```text
Gemini 2.5 Flash
```

## Embedding Models

Local:

```text
nomic-embed-text
```

Cloud:

```text
models/gemini-embedding-001
```

## Vector Database

```text
FAISS
```

## Search Provider

```text
SERP API
```

---

# Current Capabilities

Completed:

* PDF Loading
* Text Chunking
* Embeddings
* FAISS Vector Store
* Retriever
* LangGraph Migration
* Document Grading
* Conditional Routing
* Web Search Fallback
* Source Attribution
* Source Display
* Structured Output Parsing
* Retrieval Debugging
* Performance Benchmarking
* Gemini Integration

---

# Retrieval Improvements

Implemented:

* Retrieval diagnostics
* Ranking analysis
* Top-k filtering
* Document grading optimization
* MMR experimentation

Current focus:

* Retrieval ranking
* Query rewriting
* Hybrid Search
* Corrective RAG

---

# Future Roadmap

## Query Rewriting

```text
Question
↓
Rewrite Query
↓
Retrieve
↓
Answer
```

Example:

```text
Tom M. Mitchell's Definition
```

↓

```text
Tom M. Mitchell machine learning definition
```

---

## Hybrid Search

Combine:

```text
Vector Search
+
BM25
```

to improve retrieval of names, entities, and exact keywords.

---

## Corrective RAG (CRAG)

```text
Question
↓
Retrieve
↓
Grade
↓
Not Relevant
↓
Rewrite
↓
Retrieve Again
↓
Answer
```

---

## Self-Correcting RAG

```text
Question
↓
Retrieve
↓
Generate
↓
Answer Grader
↓
Retry if Needed
↓
Final Answer
```

---

# Learning Journey

This project was intentionally built incrementally:

```text
PDF Loading
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
Tool Calling Agent
↓
LangGraph
↓
Agentic RAG
↓
Corrective RAG
↓
Self-Correcting Systems
```

The objective is to understand how production-grade AI applications are built from first principles rather than relying solely on pre-built abstractions.
