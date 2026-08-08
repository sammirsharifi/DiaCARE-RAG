# DiaCARE-RAG — Version 1

## Overview

**DiaCARE-RAG Version 1** is the first implementation of the project, providing a manually implemented **GraphRAG-based system for diabetes question answering**.

This version consists of two main parts:

- **Backend** — knowledge graph construction, retrieval, LLM-based answer generation, and API.
- **Frontend** — a simple web interface for interacting with the system.

The main goal of Version 1 is to establish the initial knowledge-grounded RAG framework that will serve as the foundation for future versions.

---

## Project Structure

```text
Version 1/
│
├── ExplainableCKG/
│   └── Backend
│
└── frontend/
    └── Frontend
```

---

## Backend

The backend is implemented in Python and provides the main GraphRAG functionality.

### Knowledge Graph

Responsible for loading the medical ontology and constructing the knowledge graph used as the external knowledge source.

Main components include:

- Ontology loading
- Graph construction
- Graph management and caching
- Node mapping

### Retrieval

Responsible for finding relevant medical concepts and retrieving the corresponding evidence from the knowledge graph.

Main components include:

- Medical entity extraction
- Entity linking
- Graph-based retrieval
- Evidence subgraph extraction

### LLM

Responsible for generating the final answer using the retrieved medical evidence.

The retrieved graph evidence is provided to the Language Model so that the generated response is grounded in the external knowledge source.

### Pipeline

Connects the different components and coordinates the overall question-answering process.

```text
Question
   ↓
Entity Extraction & Linking
   ↓
Graph Retrieval
   ↓
Evidence
   ↓
LLM
   ↓
Answer
```

### API

The backend exposes the system through a **FastAPI** server, allowing the frontend to communicate with the GraphRAG system.

---

## Frontend

The frontend provides a simple web-based interface for interacting with the backend.

It is responsible for:

- Sending user questions to the backend
- Displaying generated answers
- Presenting retrieved evidence
- Providing a ChatGPT-like interaction experience

The frontend is implemented using **React / Vite**.

---

## Running Version 1

### 1. Backend

Navigate to:

```bash
cd "Version 1/ExplainableCKG"
```

Install `uv`:

```bash
pip install uv
```

Install the project dependencies:

```bash
uv sync
```

Run the FastAPI server:

```bash
uv run uvicorn explainable_graphrag.api.server:app --reload
```

The backend will start in development mode.

---

### 2. Frontend

Open another terminal and navigate to:

```bash
cd "Version 1/frontend"
```

Install the dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend can then be opened using the local address provided by Vite.

---

## Version 1 Status

Version 1 represents the **initial manually implemented GraphRAG architecture** of DiaCARE-RAG.

Future versions will improve this implementation and progressively introduce more advanced GraphRAG capabilities and, eventually, **causality-aware retrieval**.