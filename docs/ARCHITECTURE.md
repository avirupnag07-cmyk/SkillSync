# SkillSync Architectural Specification

SkillSync is an open-source, AI-powered real-time skill gap intelligence platform. This document outlines the technical design, mathematical scoring formulas, agentic orchestration pipelines, and system interfaces.

---

## 1. Multi-Agent Orchestration Architecture

SkillSync utilizes a modular **LangGraph** state machine that coordinates 6 specialized agents:

```
[Candidate Resume / Text]
          │
          ▼
┌───────────────────────────────┐
│   Resume Intelligence Agent   │ ──► Extracts identity, qualifications, projects
└───────────────────────────────┘
          │
          ▼
┌───────────────────────────────┐
│     Job Search & Ingestion    │ ──► Ingests Remotive, Arbeitnow & benchmark jobs
└───────────────────────────────┘
          │
          ▼
┌───────────────────────────────┐
│   Skill Extraction Agent      │ ──► Identifies mandatory vs. preferred requirements
└───────────────────────────────┘
          │
          ▼
┌───────────────────────────────┐
│   Skill Gap Analysis Agent    │ ──► Computes deterministic compatibility & category deltas
└───────────────────────────────┘
          │
          ▼
┌───────────────────────────────┐
│  Market Intelligence Agent    │ ──► Contextualizes against industry-wide frequencies
└───────────────────────────────┘
          │
          ▼
┌───────────────────────────────┐
│ Learning Recommendation Agent │ ──► Builds personalized weekly milestone curriculum
└───────────────────────────────┘
```

### Specialized Agents Overview
1. **Resume Intelligence Agent** (`backend/app/agents/resume_agent.py`):
   - Ingests PDF and DOCX streams via standard library XML decoders and PyPDF.
   - Extracts candidate identity, contact information, total experience years, and technical competencies.
2. **Job Search & Ingestion Agent** (`backend/app/agents/job_agent.py`):
   - Queries live public endpoints (Remotive, Arbeitnow) and maps curated benchmark roles.
   - Cleans HTML markup, normalizes salary tiers, and standardizes location data.
3. **Skill Extraction & Normalization Agent** (`backend/app/agents/skill_agent.py`):
   - Resolves colloquial aliases (`JS` -> `JavaScript`, `K8s` -> `Kubernetes`, `psql` -> `PostgreSQL`).
   - Classifies document sections into **Mandatory** (`is_mandatory: True`) vs. **Preferred** (`is_mandatory: False`).
   - Parses required experience years per skill.
4. **Skill Gap Analysis Agent** (`backend/app/agents/gap_agent.py`):
   - Evaluates multi-factor semantic alignment between candidate capabilities and job specifications.
   - Outputs 4 categorized matrices: Matched, Transferable (Partial), Missing Mandatory, and Missing Preferred.
5. **Market Intelligence Agent** (`backend/app/agents/market_agent.py`):
   - Aggregates requirement occurrences across postings to compute prevalence rankings and domain shares.
   - Calculates cross-role transition deltas (e.g. AI Engineer vs. Data Scientist).
6. **Learning Recommendation Agent** (`backend/app/agents/roadmap_agent.py`):
   - Maps identified deficits into sequenced weekly milestones.
   - Links verified official documentation and free university courses (MIT OCW, Stanford, freeCodeCamp).

---

## 2. Mathematical Compatibility Formulation

To ensure transparency and eliminate stochastic hallucinations, SkillSync evaluates compatibility using a deterministic mathematical model:

$$\text{Score} = \left( 0.60 \times \mathcal{M}_{\text{coverage}} + 0.25 \times \mathcal{P}_{\text{coverage}} + 0.15 \times \mathcal{E}_{\text{ratio}} \right) \times 100$$

### Subcomponent Calculations:
1. **Mandatory Coverage ($\mathcal{M}_{\text{coverage}}$)**:
   $$\mathcal{M}_{\text{coverage}} = \frac{\sum_{s \in \mathcal{M}} w_s \cdot \text{Sim}(s)}{\sum_{s \in \mathcal{M}} w_s}$$
   Where:
   - $\mathcal{M}$ = Mandatory skills required by the job posting.
   - $w_s \in [1.0, 2.5]$ = Skill importance weight assigned by domain centrality.
   - $\text{Sim}(s) \in [0.0, 1.0]$ = Match coefficient:
     - Exact or Alias match: $1.0$
     - Semantic Transferable match: $0.50 \le \text{Sim} < 0.98$ (e.g. React $\rightarrow$ Next.js $= 0.85$, Docker $\rightarrow$ Kubernetes $= 0.85$)
     - Missing: $0.0$

2. **Preferred Coverage ($\mathcal{P}_{\text{coverage}}$)**:
   $$\mathcal{P}_{\text{coverage}} = \frac{\sum_{s \in \mathcal{P}} w_s \cdot \text{Sim}(s)}{\sum_{s \in \mathcal{P}} w_s}$$

3. **Experience Alignment Ratio ($\mathcal{E}_{\text{ratio}}$)**:
   $$\mathcal{E}_{\text{ratio}} = \min\left(1.0, \frac{\text{Candidate Experience Years}}{\text{Required Experience Years}}\right)$$

### Alignment Tiers:
- **$\ge 85\%$**: *High Alignment* (Direct fit for core architecture and workflows)
- **$70\% - 84\%$**: *Strong Contender with Addressable Gaps* (Competitive candidate with high-leverage transferable skills)
- **$50\% - 69\%$**: *Moderate Alignment* (Foundations present; requires focused upskilling)
- **$< 50\%$**: *Requires Structured Upskilling* (Substantial skill delta; full learning roadmap recommended)

---

## 3. Technology Stack & Directory Structure

```
SkillSync/
├── frontend/               # Next.js 14 App Router, TypeScript, Tailwind CSS, Recharts
│   ├── app/                # 8 Platform Pages (Overview, Profile, Jobs, Gap, Market, Roadmap, Compare, Reports)
│   ├── components/         # Design system & interactive chart components
│   └── lib/                # API client, types, and sample datasets
├── backend/                # FastAPI, SQLAlchemy, Pydantic v2, ReportLab
│   ├── app/
│   │   ├── agents/         # LangGraph agents & workflow graph
│   │   ├── services/       # Taxonomy, scoring, resume parser, job APIs, report exports
│   │   ├── api/v1/         # REST API endpoints
│   │   └── tests/          # Pytest test suite (21 unit & integration tests)
├── sample_data/            # PDF and DOCX sample resumes and benchmark jobs
├── docker-compose.yml      # Multi-container orchestration (PostgreSQL, Backend, Frontend, Ollama)
└── .env.example            # Documented environment defaults
```
