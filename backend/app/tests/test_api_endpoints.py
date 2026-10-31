"""Integration tests for FastAPI REST endpoints."""

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db

init_db()
client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "active_provider" in data
    assert data["database"] == "connected"


def test_guest_auth_endpoint():
    response = client.post("/api/v1/auth/guest")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["is_guest"] is True


def test_skills_taxonomy_endpoint():
    response = client.get("/api/v1/skills/taxonomy")
    assert response.status_code == 200
    data = response.json()
    assert data["total_skills"] > 20
    assert "languages" in data["categories"]


def test_jobs_benchmark_endpoint():
    response = client.get("/api/v1/jobs/benchmark")
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) >= 4
    assert any("AI" in j["title"] for j in jobs)


def test_gap_analyze_endpoint():
    payload = {
        "candidate_skills": [
            {"id": "python", "name": "Python"},
            {"id": "docker", "name": "Docker"}
        ],
        "raw_job_description": "Minimum Qualifications: Python, Docker, Kubernetes, AWS.",
        "job_title": "Platform Engineer"
    }
    response = client.post("/api/v1/gap/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert len(data["matched_skills"]) >= 2
    assert len(data["partially_matched_skills"]) >= 1  # Kubernetes via Docker
    assert len(data["missing_mandatory_skills"]) >= 1  # AWS
    assert "disclaimer" in data


def test_market_overview_endpoint():
    response = client.get("/api/v1/market/overview")
    assert response.status_code == 200
    data = response.json()
    assert len(data["top_skills"]) > 0
    assert len(data["category_distribution"]) > 0


def test_role_comparison_endpoint():
    response = client.get("/api/v1/comparison/compare?role_a=ai_engineer&role_b=data_scientist")
    assert response.status_code == 200
    data = response.json()
    assert "role_a" in data
    assert "role_b" in data
    assert "shared_skills" in data
    assert "overlap_percentage" in data
