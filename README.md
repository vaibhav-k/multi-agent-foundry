# Microsoft Foundry Multi-Agent System

A reference implementation for building an enterprise multi-agent AI application using **Microsoft AI Foundry**, Azure-hosted models, RAG capabilities, AI safety controls, and evaluation workflows.

The goal of this project is to establish a scalable foundation for:

- Multi-agent orchestration
- Retrieval-Augmented Generation (RAG)
- Tool-enabled AI agents
- Prompt governance
- AI safety and guardrails
- RAG evaluation
- Monitoring and observability

---

# Project Status

## Current Phase: Day 1 Foundation

Implemented:

- ✅ Microsoft AI Foundry model connectivity
- ✅ Environment-based configuration
- ✅ Azure AI Foundry client setup
- ✅ Base agent framework
- ✅ Planner Agent
- ✅ Agent orchestration layer
- ✅ Chat connectivity validation
- ✅ Embedding connectivity validation

Planned phases:

- Knowledge Agent
- Action Agent
- RAG pipeline
- Vector search integration
- MCP/tool governance
- Content Safety integration
- RAG evaluation framework
- Application Insights monitoring
- CI/CD deployment

---

# Solution Overview

The system follows a multi-agent architecture where specialized agents collaborate to solve user requests.

Initial architecture:

                User
                 |
                 |
                 v

          Orchestrator

                 |
                 |
                 v

          Planner Agent

                 |
                 |
                 v

      Microsoft AI Foundry Model

                 |
                 |
                 v

          Agent Response


Future architecture:

                     User
                      |
                      |
                      v

              Agent Orchestrator

                      |
                      |
                      v

               Planner Agent

             /              \
            /                \
           v                  v

  Knowledge Agent          Action Agent

         |                     |
         |                     |
         v                     v

   RAG Knowledge          Enterprise Tools
   Base                   APIs / MCP Tools


---

# Technology Stack

| Area | Technology |
|---|---|
| AI Platform | Microsoft AI Foundry |
| Language Models | Azure-hosted Foundry models |
| Embeddings | Azure embedding models |
| SDK | OpenAI Python SDK |
| Language | Python |
| Configuration | python-dotenv |
| Data Models | Pydantic |
| Testing | Pytest |
| Future Vector Search | Azure AI Search |
| Monitoring | Application Insights |
| Security | Microsoft Entra ID, Azure AI Content Safety |

---

# Repository Structure

multi-agent-foundry/

│
├── src/
│ │
│ ├── agents/
│ │ ├── init.py
│ │ ├── base.py
│ │ └── planner.py
│ │
│ ├── config/
│ │ ├── init.py
│ │ ├── settings.py
│ │ └── client.py
│ │
│ ├── orchestrator/
│ │ ├── init.py
│ │ └── orchestrator.py
│ │
│ ├── models.py
│ ├── main.py
│ └── init.py
│
├── tests/
│ ├── test_chat.py
│ └── test_embeddings.py
│
├── docs/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md


---

# Prerequisites

Before running this project, ensure you have:

## Required Software

- Python 3.11 or later
- Git
- Azure subscription

## Azure Requirements

You need:

- Microsoft AI Foundry project
- Chat model deployment
- Embedding model deployment
- API credentials

Example deployments:

| Purpose | Deployment |
|---|---|
| Chat | gpt-5.2 |
| Embeddings | text-embedding-3-small |

---

# Azure AI Foundry Setup

## 1. Create Foundry Project

Create a project in Microsoft AI Foundry.

Example endpoint:

https://<project-name>.services.ai.azure.com


---

## 2. Deploy Models

Deploy:

### Chat Model

Example:

```
gpt-5.2
```


Used by:

- Planner Agent
- Knowledge Agent
- Action Agent

---

### Embedding Model

Example:

```
text-embedding-3-small
```


Used by:

- Document processing
- Semantic search
- RAG retrieval

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
FOUNDRY_ENDPOINT=https://<project>.services.ai.azure.com/openai/v1

FOUNDRY_API_KEY=<your-api-key>

CHAT_DEPLOYMENT=gpt-5.2

EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

# Installation

Clone Repository

```bash
git clone <repository-url>
cd multi-agent-foundry
```

# Create Virtual Environment

## Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Linux/Mac:

```bash
python -m venv .venv
source .venv/bin/activate
```

# Install Dependencies

```bash
pip install -r requirements.txt
```

# Running the Application

Execute:

```bash
python -m src.main
```

Example flow:

User Request

        |
        v

Orchestrator

        |
        v

Planner Agent

        |
        v

Azure AI Foundry

        |
        v

Response

Example output:

```bash
Agent   : PlannerAgent

Response:
Microsoft AI Foundry provides tools and services
for building and deploying AI applications.
```
