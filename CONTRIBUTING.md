# Contributing to SkillSync

Thank you for your interest in contributing to SkillSync! We are building an open-source, AI-powered real-time skill gap intelligence platform to democratize career growth and technical upskilling.

## Code of Conduct
We are committed to providing a welcoming, inclusive, and harassment-free environment for all contributors.

## Architecture Philosophy
- **Deterministic-First Core**: We use fast, explainable deterministic algorithms for skill normalization, counting, comparison, and mathematical scoring rather than wasting LLM calls on simple math.
- **Transparent AI Reasoning**: SkillSync supports local open-weight models via Ollama (Qwen, Llama 3, Mistral) and cloud providers. The platform must remain 100% functional without API keys. Never pretend an AI model is running when it is not.
- **Production Craft**: Minimalist, high-density UI inspired by Linear and Vercel. Avoid bloated cards, unnecessary glassmorphism, or non-functional mock buttons.

## Local Development Setup

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Docker Compose (Single Command Launch)
```bash
docker compose up --build
```

## Running the Test Suite
```bash
cd backend
pytest app/tests -v
```

## Pull Request Guidelines
1. Fork the repository and create your feature branch from `main`.
2. Write unit tests covering new skills, agents, or scoring formulas.
3. Ensure all tests pass (`pytest`) and Next.js builds without warnings (`npm run build`).
4. Submit your pull request with a concise architectural explanation.
