# Law Entropy

An intelligent analysis system for regulatory legal acts (RLAs) of the Republic of Kazakhstan. The project identifies legal conflicts, outdated regulations, and visualizes document relationships using graph theory and natural language processing.

---

### 🛡️ Academic & Technical Overview

This project was developed as a hackathon MVP demonstrating applied concepts in **Data Analysis, Graph Theory, and Information Security**:

* **Conflict & Anomaly Detection:** Applies NLP techniques and multi-provider LLM pipelines to perform semantic comparison and automated contradiction detection across complex textual datasets.
* **Graph-Based Structural Modeling:** Leverages **D3.js** for interactive knowledge graph rendering, modeling hierarchy, dependencies, and reference integrity between entities.
* **Low-Level Performance Optimization:** Core parsing and computational modules integrate **C / Cython** extensions alongside Python (FastAPI) for high-performance processing.
* **Multi-Provider LLM Integration:** Feature-rich AI backend supporting dynamic failover and integration with Google Gemini, DeepSeek, Groq, OpenAI, and Anthropic.

> **Project Status:** *Completed (Archived MVP)*. Built to demonstrate graph visualization, multi-LLM orchestration, and low-level code optimization.

---

## Key Features

* **Conflict Search:** Direct comparison of multiple regulatory documents to identify logical, procedural, and legal contradictions.
* **Outdated Norm Detector:** Automated identification of references to repealed or invalidated acts.
* **Interactive Knowledge Graph:** Dependency and hierarchy visualization using D3.js.
* **AI Assistant:** Context-aware interactive Q&A assistant over uploaded legal documents.
* **Multilingual Support:** Full interface and analysis support for Kazakh, Russian, and English.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, Vanilla JS, D3.js (Graph Visualization), PDF.js, Mammoth.js |
| **Proxy / Web Server** | Node.js, Express (CORS bypass, static serving) |
| **Backend & Core** | Python 3.11, FastAPI, Cython, C extensions, BeautifulSoup4 |
| **AI Providers** | Google Gemini, DeepSeek, Groq, OpenAI, Anthropic, AlemLLM |
| **Infrastructure** | Docker, Docker Compose |

---

## Quick Start (Docker)

The easiest way to run the project is via Docker Compose. It spins up both the Node.js frontend/proxy and Python parsing backend simultaneously.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Build and launch the containers:
   ```bash
   docker-compose up --build

## Manual Setup (For Development)

### 1. Frontend & Proxy (Node.js)
```bash
npm install
npm start
```
Сервер будет доступен на порту 3000.

### 2. Backend Engine (Python)
```bash
cd backend
python -m venv venv
source venv/bin/activate # или venv\Scripts\activate in Windows
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
## Licence

This project is distributed under the MIT licence.
