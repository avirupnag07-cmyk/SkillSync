# SkillSync ⚡

> **AI-Powered Real-Time Skill Gap Intelligence & Adaptive Learning Platform**  
> An open-source, production-ready full-stack web application designed to bridge the gap between engineering capabilities and real-world job requirements.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js_14_App_Router-black)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_Python_3.11-009688)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_16-336791)](https://www.postgresql.org)
[![LangGraph](https://img.shields.io/badge/Agentic_Core-LangGraph_Orchestrator-orange)](https://langchain-ai.github.io/langgraph/)
[![Tests](https://img.shields.io/badge/Tests-21%2F21_Passed-brightgreen)](backend/app/tests)

---

## 🌟 Overview

**SkillSync** is an AI-powered intelligence platform that analyzes resumes, maps real-time industry job requirements from live public feeds (Remotive, Arbeitnow), computes an explainable career compatibility score, and generates customized weekly milestone learning roadmaps.

Inspired by the design aesthetics of **Linear**, **Vercel**, and **Stripe Analytics**, SkillSync delivers a high-craft, restrained visual interface featuring an off-white canvas, crisp charcoal typography, subtle borders, interactive Recharts visualizations, and electric blue micro-accents.

---

## 🚀 Key Modules & Product Functionality

### 1. 📄 Career Profile & Document Ingestion
- **Multi-Format Ingestion**: Drag-and-drop resumes in **PDF**, **Word (.docx)**, or plain text.
- **Resume Intelligence Agent**: Decodes document structures to extract contact identity, total experience years, employment history, and technical competencies.
- **Interactive Competency Editor**: Add, verify, or remove skill tags; edit employment milestones and portfolio project repositories.
- **1-Click Demo Profiles**: Pre-loaded with verified industry profiles (*Maya Chen - Senior AI*, *Marcus Vance - Staff Full Stack*, *Elena Rostova - DevOps Lead*).

### 2. 💼 Job Intelligence & Requirement Feeds
- **Unified Remote Search**: Search postings filtered by keywords, technical stack, and geographic location.
- **Legitimate Public APIs**: Ingest live opportunities directly from **Remotive** and **Arbeitnow** public job feeds.
- **Curated Benchmark Roles**: Pre-verified real-world industry specifications across AI Systems Engineering, Staff Full Stack, Cloud Infrastructure, and Quantitative Data Science.
- **Manual Specification Paste**: Paste custom job listings with real-time requirement extraction and mandatory vs. preferred classification.

### 3. 🧠 Skill Extraction & Ontology Normalization
- **450+ Canonical Ontology**: Comprehensive technical taxonomy covering Languages, Frameworks, Cloud & DevOps, Databases, AI/ML, Developer Tools, and Soft Skills.
- **Alias Resolution Engine**: Automatically normalizes equivalent terms (`JS` $\rightarrow$ `JavaScript`, `K8s` $\rightarrow$ `Kubernetes`, `psql` $\rightarrow$ `PostgreSQL`, `sklearn` $\rightarrow$ `Scikit-Learn`, `TF` $\rightarrow$ `TensorFlow`).
- **Contextual Requirement Classification**: Differentiates between strict mandatory requirements and preferred bonus qualifications.

### 4. 🎯 Skill Gap Analysis & Explainable Compatibility
- **Deterministic Multi-Factor Scoring**: Evaluates candidates mathematically without hallucinated probabilities.
- **Categorized Requirement Matrices**:
  - **Matched Skills**: Direct capability match ($\text{Sim} = 1.0$).
  - **Transferable / Partially Matched Skills**: Identified transferable substitutes ($\text{Sim} \ge 0.5$, e.g., React $\rightarrow$ Next.js, PyTorch $\rightarrow$ TensorFlow).
  - **Missing Mandatory Skills**: Highest-priority technical gaps impacting employability.
  - **Missing Preferred Skills**: Secondary bonus qualifications.
  - **Unverified Skills**: Self-reported competencies lacking project attribution.
- **Visual Diagnostics**: Circular Score Gauge, multi-tier progress bars, and Recharts 8-domain radar charts.
- **Career Advisory Disclaimer**: Transparently notes that scores represent semantic requirement alignment rather than employment guarantees.

### 5. 📊 Market Intelligence & Demand Trends
- **Prevalence Leaderboard**: Top 20 most demanded technologies across active job postings with frequency counts and mandatory-to-preferred ratios.
- **Domain Distribution Donut**: Visual share of requirements by architectural layer (Languages, Frameworks, Data, Cloud, AI).
- **Emerging Technologies Pulse**: High-growth skills index (*LangGraph: +185% YoY*, *RAG: +140% YoY*, *Vector DBs: +115% YoY*).

### 6. 🗺️ Personalized Learning Roadmap
- **Adaptive Weekly Curriculum**: Generates a 4, 6, 8, or 12-week progressive curriculum targeting identified gaps.
- **Pedagogical Progression**: Foundational syntax $\rightarrow$ core frameworks $\rightarrow$ specialized cloud/AI systems $\rightarrow$ capstone verification.
- **Verified Learning Links**: Direct links to official documentation (Python, FastAPI, PyTorch, React, Kubernetes) and free high-quality courses (Harvard CS50, freeCodeCamp, Stanford, DeepLearning.AI).
- **Hands-On Milestone Projects**: Clear specifications for proof-of-work portfolio deliverables.
- **Interactive Task Checklist**: Check off completed learning tasks to track progress in real time with state persistence.

### 7. ⚖️ Cross-Role Career Comparison
- **Tri-Column Comparison**: Side-by-side competency delta between engineering tracks (e.g. *AI Engineer* vs. *Data Scientist* vs. *Data Engineer*).
- **Transition Delta Index**: Quantifies the skill gap and overlap percentage between origin and destination roles.
- **Strategic Advisory**: Recommends high-leverage technologies to focus on during a career shift.

### 8. 📑 Audit-Ready Reports & Exports
- **Vector PDF Documents**: Rendered using ReportLab with corporate styling, score callouts, and explainability summaries.
- **RFC 4180 CSV Tables**: Clean, standardized tabular data for ATS integration or spreadsheet analysis.

---

## 📐 Mathematical Compatibility Formulation

The compatibility engine evaluates alignment using a deterministic mathematical model:

$$\text{Score} = \left( 0.60 \times \frac{\sum_{s \in \mathcal{M}} w_s \cdot \text{Sim}(s)}{\sum_{s \in \mathcal{M}} w_s} + 0.25 \times \frac{\sum_{s \in \mathcal{P}} w_s \cdot \text{Sim}(s)}{\sum_{s \in \mathcal{P}} w_s} + 0.15 \times \min\left(1.0, \frac{\text{Candidate Exp}}{\text{Required Exp}}\right) \right) \times 100$$

- $\mathcal{M}$: Mandatory job requirements
- $\mathcal{P}$: Preferred qualifications
- $w_s$: Importance weight factor ($1.0$ to $2.5$)
- $\text{Sim}(s)$: Semantic match coefficient ($1.0$ for exact/alias, $0.5 - 0.95$ for transferable skills, $0.0$ for missing)

---

## 🤖 AI Agent Architecture & Transparency

SkillSync coordinates specialized agents via a modular **LangGraph** orchestration graph:

1. **Resume Intelligence Agent**
2. **Job Search & Ingestion Agent**
3. **Skill Extraction & Normalization Agent**
4. **Skill Gap Analysis Agent**
5. **Market Intelligence Agent**
6. **Learning Recommendation Agent**

### Zero-Key Portability Guarantee
- **Local Open-Weight Models**: Direct support for **Ollama** runtimes (Qwen, Llama 3, Mistral) via `OLLAMA_BASE_URL`.
- **Cloud LLM APIs**: Optional integration with OpenAI, Gemini, or Groq via environment variables.
- **Deterministic Reasoning Engine**: When no external keys or daemons are present, SkillSync automatically operates via its built-in deterministic rule and semantic ontology engine. **The application never fabricates AI inference and remains 100% functional out of the box.**
- **Transparent Status Badge**: The UI header displays a live indicator indicating the active provider (e.g., `Deterministic Engine (No API Key Required)` or `Local LLM: llama3`).

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons, Recharts, Framer Motion |
| **Backend** | FastAPI, Python 3.11, SQLAlchemy 2.0, Pydantic v2, ReportLab, PyPDF, python-docx |
| **Database** | PostgreSQL 16 (production container) / SQLite (zero-config local fallback) |
| **Agent Core** | LangGraph Agent Workflow, Deterministic Ontology Graph |
| **DevOps** | Docker, Docker Compose, Health Checks, Non-root secure containers |

---

## 🐳 Quick Start with Docker (Single Command)

You can launch the entire stack (PostgreSQL database, FastAPI backend, and Next.js frontend) with a single command:

```bash
# 1. Clone repository
git clone https://github.com/avirupnag07-cmyk/c-practice.git SkillSync
cd SkillSync

# 2. Configure environment
cp .env.example .env

# 3. Launch application
docker compose up --build
```

Once running:
- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend & Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Diagnostics**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

*(To launch with local Ollama service enabled: `docker compose --profile with-ollama up --build`)*

---

## 🚀 Local Deployment Guide

Anyone can clone and run SkillSync locally on their machine within minutes. You can choose either the **One-Command Docker Deployment** (recommended) or the **Native Local Setup**.

---

### Prerequisites
Before starting, ensure you have the following installed on your machine:

- **For Docker Deployment**:
  - [Docker](https://docs.docker.com/get-docker/) (v20.10+)
  - [Docker Compose](https://docs.docker.com/compose/) (v2.0+)
- **For Native Local Setup**:
  - [Node.js](https://nodejs.org/) (v18.0+ or v20.x recommended) and `npm`
  - [Python](https://www.python.org/) (v3.9, 3.10, or 3.11) and `pip`
  - (Optional) [PostgreSQL](https://www.postgresql.org/) (if not using the default zero-config SQLite mode)
  - (Optional) [Ollama](https://ollama.com/) (if you wish to run local LLMs like Llama 3 or Qwen)

---

### Method A: One-Command Docker Deployment (Recommended)

This runs the PostgreSQL database, FastAPI backend, and Next.js frontend in isolated containers with automated database migrations and health checks.

```bash
# 1. Clone the repository
git clone https://github.com/avirupnag07-cmyk/SkillSync.git
cd SkillSync

# 2. Create your environment configuration file
cp .env.example .env

# 3. Build and launch all services
docker compose up --build
```

> [!TIP]
> To run the containers in detached (background) mode, use:
> ```bash
> docker compose up -d --build
> ```
> To stop the services: `docker compose down`

#### Optional: Run with Local Ollama Container
If you want Docker to also spin up an Ollama container for local open-weight models:
```bash
docker compose --profile with-ollama up --build
```

---

### Method B: Native Local Setup (Without Docker)

You can run SkillSync directly on your machine using two terminal tabs. In local mode, the backend defaults to SQLite (`sqlite:///./skillsync.db`), meaning no database installation is required!

#### Step 1: Backend Setup (Terminal 1)
```bash
# 1. Navigate to the backend directory
cd SkillSync/backend

# 2. Create and activate a Python virtual environment
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell):
# python -m venv venv
# .\venv\Scripts\Activate.ps1

# 3. Install required Python packages
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify the test suite (optional but recommended)
pytest app/tests -v

# 5. Start the FastAPI backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*The backend API will now be running at: `http://localhost:8000` (Swagger Docs: `http://localhost:8000/docs`)*

---

#### Step 2: Frontend Setup (Terminal 2)
```bash
# 1. Open a new terminal and navigate to the frontend directory
cd SkillSync/frontend

# 2. Install Node dependencies
npm install

# 3. (Optional) Create .env.local if you changed the backend port:
# echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local

# 4. Start the Next.js development server
npm run dev
```
*The frontend interface will now be live at: `http://localhost:3000`*

---

### 🌐 Accessing the Application

| Service | Local URL | Description |
| :--- | :--- | :--- |
| **Web Dashboard** | [http://localhost:3000](http://localhost:3000) | Complete Next.js user interface |
| **Interactive API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI for testing all REST endpoints |
| **ReDoc Specification** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Alternative OpenAPI documentation |
| **Health Diagnostics** | [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) | Live engine status and LLM provider info |

---

### ⚡ Verification & Step-by-Step Demo Walkthrough

Once both services are running:

1. **Dashboard Overview (`/`)**: Open [http://localhost:3000](http://localhost:3000) to see executive market metrics. Click any of the pre-loaded sample profiles (e.g. *Maya Chen - Senior AI*) to load immediate test data.
2. **Career Profile (`/profile`)**: Test the resume parser by dragging-and-dropping one of the sample PDF resumes located in `sample_data/resumes/maya_chen_ai_engineer.pdf`. Observe how skills, experience, and contact details are automatically parsed and displayed.
3. **Job Intelligence (`/jobs`)**: Search remote jobs using Remotive and Arbeitnow APIs, view curated benchmark roles, or paste any custom job description.
4. **Skill Gap Analysis (`/gap-analysis`)**: Select your profile and target job, click **"Recalculate Gap Analysis"**, and watch the circular compatibility gauge, 8-domain radar chart, and categorized matrices render in real time.
5. **Market Analytics (`/market`)**: Review the top in-demand skills leaderboard and interactive Recharts visualizations.
6. **Learning Roadmap (`/roadmap`)**: View your personalized weekly milestones curriculum and check off tasks to test interactive progress tracking.
7. **Role Comparison (`/role-comparison`)**: Compare careers like AI Engineer vs. Data Scientist side-by-side.
8. **Reports & Exports (`/reports`)**: Click **"Download PDF Document"** or **"CSV"** to test live document streaming.

---

### 🔧 Troubleshooting & Common Questions

- **Port 3000 or 8000 is already in use**:
  - You can change the frontend port by running `npm run dev -- -p 3001` or the backend port by adding `--port 8080` to `uvicorn`. Update `NEXT_PUBLIC_API_URL` accordingly.
- **Do I need an OpenAI or Gemini API key to run SkillSync?**:
  - **No.** SkillSync features a built-in deterministic rule and ontology engine with 450+ canonical skills and semantic similarity mappings. The entire workflow operates out of the box with zero external API keys.
- **Can I use local Ollama models?**:
  - Yes! If you have Ollama running locally (`ollama run llama3`), SkillSync will automatically detect it at `http://localhost:11434` and use it for agent reasoning, visible on the top header badge.

---

## 🧪 Automated Testing & Diagnostics

SkillSync includes an automated test suite verifying ontology normalization, semantic similarity, multi-factor compatibility scoring, resume parsing, agent orchestration, and REST API endpoints:

```bash
backend/venv/bin/pytest backend/app/tests -v
```

**Test Results Summary**:
```
collected 21 items

backend/app/tests/test_api_endpoints.py::test_health_check_endpoint PASSED    [  4%]
backend/app/tests/test_api_endpoints.py::test_guest_auth_endpoint PASSED     [  9%]
backend/app/tests/test_api_endpoints.py::test_skills_taxonomy_endpoint PASSED[ 14%]
backend/app/tests/test_api_endpoints.py::test_jobs_benchmark_endpoint PASSED  [ 19%]
backend/app/tests/test_api_endpoints.py::test_gap_analyze_endpoint PASSED    [ 23%]
backend/app/tests/test_api_endpoints.py::test_market_overview_endpoint PASSED[ 28%]
backend/app/tests/test_api_endpoints.py::test_role_comparison_endpoint PASSED[ 33%]
backend/app/tests/test_gap_agent.py::test_agent_workflow_execution PASSED    [ 38%]
backend/app/tests/test_market_agent.py::test_market_demand_analysis PASSED   [ 42%]
backend/app/tests/test_market_agent.py::test_role_comparison PASSED         [ 47%]
backend/app/tests/test_report_generator.py::test_gap_csv_generation PASSED    [ 52%]
backend/app/tests/test_report_generator.py::test_gap_pdf_generation PASSED    [ 57%]
backend/app/tests/test_report_generator.py::test_roadmap_csv_generation PASSED[ 61%]
backend/app/tests/test_report_generator.py::test_roadmap_pdf_generation PASSED[ 66%]
backend/app/tests/test_resume_parser.py::test_contact_extraction PASSED     [ 71%]
backend/app/tests/test_resume_parser.py::test_resume_document_parsing PASSED [ 76%]
backend/app/tests/test_scoring.py::test_perfect_compatibility_score PASSED    [ 80%]
backend/app/tests/test_scoring.py::test_partial_and_missing_skills PASSED     [ 85%]
backend/app/tests/test_skill_taxonomy.py::test_alias_normalization PASSED    [ 90%]
backend/app/tests/test_skill_taxonomy.py::test_skill_metadata_retrieval PASSED[ 95%]
backend/app/tests/test_skill_taxonomy.py::test_skill_similarity PASSED      [100%]

============================== 21 passed in 0.36s ==============================
```

---

## 📁 Repository Structure

```
SkillSync/
├── frontend/                     # Next.js 14 App Router, TypeScript, Tailwind CSS
│   ├── app/
│   │   ├── layout.tsx            # Global layout with ThemeProvider & Sidebar
│   │   ├── globals.css           # Linear design tokens & color definitions
│   │   ├── page.tsx              # Overview Executive Dashboard
│   │   ├── profile/page.tsx      # Career Profile & Resume Upload
│   │   ├── jobs/page.tsx         # Job Intelligence (Live APIs & Manual Paste)
│   │   ├── gap-analysis/page.tsx # Skill Gap Analysis & Compatibility Gauge
│   │   ├── market/page.tsx       # Market Intelligence & Demand Analytics
│   │   ├── roadmap/page.tsx      # Learning Roadmap & Interactive Task Tracker
│   │   ├── role-comparison/page.tsx # Cross-Role Career Transition Matrix
│   │   └── reports/page.tsx      # PDF and CSV Exports Hub
│   ├── components/               # Layout, Navigation, and Recharts Components
│   ├── lib/                      # Type-safe API client and sample datasets
│   └── Dockerfile
├── backend/                      # FastAPI Application
│   ├── app/
│   │   ├── main.py               # Application entrypoint & CORS middleware
│   │   ├── core/                 # Config, Database, and Security modules
│   │   ├── models/               # SQLAlchemy ORM Models
│   │   ├── schemas/              # Pydantic v2 Schemas
│   │   ├── agents/               # LangGraph Agent Orchestration
│   │   ├── services/             # Taxonomy, Scorer, APIs, and ReportLab exporters
│   │   ├── api/v1/               # Modular REST endpoints
│   │   └── tests/                # Automated Pytest suite
│   ├── requirements.txt
│   └── Dockerfile
├── sample_data/                  # Sample PDF/DOCX resumes and benchmark jobs
│   ├── resumes/
│   │   ├── ai_engineer_resume.txt
│   │   ├── maya_chen_ai_engineer.pdf
│   │   ├── fullstack_engineer_resume.txt
│   │   ├── marcus_vance_fullstack.pdf
│   │   ├── cloud_devops_resume.txt
│   │   └── elena_rostova_devops.pdf
├── docs/
│   └── ARCHITECTURE.md           # Comprehensive technical specification
├── docker-compose.yml            # Multi-service container orchestration
├── .env.example                  # Environment configuration template
├── LICENSE                       # Apache 2.0 Open Source License
├── CONTRIBUTING.md               # Contribution and coding standards
└── README.md
```

---

## 📄 License

SkillSync is distributed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for details.
