# Enterprise IT Knowledge Assistant

A production-style multi-agent RAG assistant for enterprise IT support scenarios.

The application combines:

- Planner Agent for request analysis and workflow routing
- Knowledge Agent for enterprise document retrieval and grounded answers
- Safety Agent for response validation
- Response Agent for final answer generation
- Azure AI services integration
- FastAPI HTTP API layer

---

## Architecture

```text
User Request
|
v
FastAPI API
|
v
Orchestrator
|
v
Planner Agent
|
v
PlannerDecision
|
+----------------+
|                |
v                v
Knowledge Agent     Safety Agent
|                |
v                |
Enterprise RAG        |
|                |
+-------+--------+
|
v
Response Agent
|
v
Final Response
```

---

## Features

### Multi-Agent Workflow

The assistant uses specialized agents:

### PlannerAgent

Responsibilities:

- Understand user intent
- Decide if retrieval is required
- Decide if safety validation is required
- Generate execution workflow

Flow:

```text
User Question
|
v
LLM Structured Output
|
v
PlannerDecision
|
v
Orchestrator Routing
```

---

### KnowledgeAgent

Responsibilities:

- Query enterprise knowledge base
- Retrieve relevant documents
- Rerank documents
- Generate grounded answers

Current retrieval flow:

```text
User Query
|
v
Query Rewriter
|
v
Azure AI Search / Vector Search
|
v
Document Retrieval
|
v
Grounded Answer
```

---

### SafetyAgent

Responsibilities:

- Validate generated responses
- Check grounding
- Prevent unsafe disclosure

Current validations:

- Empty response detection
- Grounding validation
- Policy validation hooks

Future integrations:

- Azure AI Content Safety
- Prompt injection detection
- PII detection

---

### ResponseAgent

Responsibilities:

- Format final response
- Include confidence
- Include sources
- Return user-friendly output

---

# Project Structure

```text
src/
|
├── agents/
│   ├── planner.py
│   ├── knowledge.py
│   ├── safety.py
│   └── response.py
|
├── orchestrator/
│   ├── orchestrator.py
│   ├── state.py
│   └── router.py
|
├── rag/
│   ├── query.py
│   ├── retriever.py
│   ├── search.py
│   ├── reranker.py
│   └── citations.py
|
├── api/
│   ├── app.py
│   ├── routes.py
│   ├── schemas.py
│   └── dependencies.py
|
├── models.py
├── main.py
└── bootstrap.py
```

---

# Requirements

Python:

```

Python 3.12+

````

Install dependencies:

```bash
pip install -r requirements.txt
````

or using uv:

```bash
uv sync
```

---

# Running Locally

## CLI Mode

Run the assistant:

```bash
python -m src.main
```

Example:

```text
How do I connect to the company VPN?
```

Output:

```text
To connect to the company VPN:

1. Open the approved company VPN client.
2. Enter your corporate username.
3. Complete MFA verification.
4. Select the VPN profile.
5. Click Connect.
```

---

# Running the API

Start FastAPI:

```bash
uvicorn src.api.app:app --reload
```

Application:

```
http://127.0.0.1:8000
```

Health:

```
http://127.0.0.1:8000/api/v1/health
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Health Check

### GET

```
/api/v1/health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Chat

### POST

```
/api/v1/chat
```

Request:

```json
{
  "conversation_id": "demo-session",
  "message": "How do I enroll in MFA?"
}
```

Response:

```json
{
  "conversation_id": "demo-session",
  "answer": "Follow the MFA enrollment steps...",
  "sources": [
    "mfa_setup.md"
  ],
  "safe": true
}
```

---

# Example Questions

The assistant supports enterprise IT questions such as:

```
How do I connect to the company VPN?
```

```
How do I enroll in MFA?
```

```
What does mobile access require?
```

```
How do I report an IT incident?
```

---

# Testing

Run all tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Current coverage areas:

* Agents
* Orchestrator
* RAG pipeline
* API schemas
* State management
* Safety validation

---

# Configuration

Environment variables:

```
# ==========================================================
# Application
# ==========================================================

LOG_LEVEL=INFO

# ==========================================================
# Azure AI Foundry Project
# ==========================================================

AZURE_AI_PROJECT_ENDPOINT=...

AZURE_OPENAI_CHAT_DEPLOYMENT=...
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=...

AZURE_INFERENCE_ENDPOINT=...
AZURE_INFERENCE_KEY=...

AZURE_SEARCH_ENDPOINT=...
AZURE_SEARCH_KEY=...
AZURE_SEARCH_INDEX=...
```

---

# Development Roadmap

## Completed

* [x] Multi-agent architecture
* [x] Planner structured workflow
* [x] RAG retrieval pipeline
* [x] Query rewriting
* [x] Document reranking
* [x] Safety validation
* [x] FastAPI API layer
* [x] Health endpoint
* [x] Automated tests

---

# Git Workflow

Run tests before committing:

```bash
pytest
```

Commit example:

```bash
git add .
git commit -m "add FastAPI API layer and improve multi-agent documentation"
```

---

# License

Internal enterprise application prototype.

````
