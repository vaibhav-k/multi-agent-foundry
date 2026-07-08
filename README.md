# Enterprise IT Knowledge Assistant using Microsoft Foundry

An enterprise-grade **Multi-Agent AI Assistant** built with **Microsoft Foundry**, **Azure OpenAI**, and **Azure AI Search**.

The assistant helps employees retrieve accurate IT knowledge from enterprise documentation using **Retrieval-Augmented Generation (RAG)** while ensuring responses remain safe, grounded, and compliant with organizational policies.

---

## Features

* Multi-Agent Architecture
* Planner Agent for request orchestration
* Knowledge Agent with RAG
* Safety Agent using Azure AI Content Safety
* Azure AI Search vector retrieval
* Modular architecture
* Evaluation framework
* Production-ready configuration
* Easy deployment to Azure

---

## Architecture

```text
                   User
                     │
                     ▼
              Planner Agent
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
 Knowledge Agent           Safety Agent
        │                         │
        ▼                         ▼
 Azure AI Search      Azure AI Content Safety
        │
        ▼
 Enterprise Documents
```

---

## Repository Structure

```text
multi-agent-foundry/

docs/
src/
tests/
evaluation/
data/

README.md
requirements.txt
.env.example
```

---

## Technology Stack

| Component  | Technology                  |
| ---------- | --------------------------- |
| Framework  | Microsoft Foundry           |
| LLM        | Azure OpenAI                |
| Search     | Azure AI Search             |
| Embeddings | text-embedding-3-large      |
| Language   | Python 3.12+                |
| Evaluation | Custom evaluation framework |

---

## Project Workflow

1. User submits a question.
2. Planner Agent determines the workflow.
3. Knowledge Agent retrieves relevant enterprise documents.
4. Safety Agent validates the generated response.
5. Final answer is returned.

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/multi-agent-foundry.git
cd multi-agent-foundry
```

### Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Copy:

```text
.env.example
```

to

```text
.env
```

Update the Azure credentials.

### Run the application

```bash
python -m src.main
```

---

## Example Questions

* How do I connect to the company VPN?
* What is the password policy?
* How do I install Visual Studio?
* Explain the remote work policy.
* Where can I find onboarding documentation?

---

## Roadmap

* [x] Planner Agent
* [ ] Knowledge Agent
* [ ] Safety Agent
* [ ] Azure AI Search Integration
* [ ] RAG Evaluation
* [ ] Deployment
* [ ] Monitoring
* [ ] CI/CD

---

## License

MIT License
