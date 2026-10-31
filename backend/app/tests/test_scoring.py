"""Unit tests for deterministic compatibility scoring and explainability metrics."""

from app.services.compatibility_scorer import compute_compatibility_score, DISCLAIMER


def test_perfect_compatibility_score():
    candidate_skills = [
        {"id": "python", "name": "Python", "verified": True},
        {"id": "fastapi", "name": "FastAPI", "verified": True},
        {"id": "postgresql", "name": "PostgreSQL", "verified": True},
    ]

    job_skills = [
        {"id": "python", "name": "Python", "is_mandatory": True, "weight": 2.0},
        {"id": "fastapi", "name": "FastAPI", "is_mandatory": True, "weight": 2.0},
        {"id": "postgresql", "name": "PostgreSQL", "is_mandatory": False, "weight": 1.5},
    ]

    result = compute_compatibility_score(
        candidate_skills=candidate_skills,
        job_skills=job_skills,
        candidate_experience_years=3.0,
        required_experience_years=3.0,
    )

    assert result["overall_score"] == 100.0
    assert result["mandatory_score"] == 100.0
    assert result["preferred_score"] == 100.0
    assert result["experience_score"] == 100.0
    assert result["alignment_tier"] == "High Alignment"
    assert len(result["missing_mandatory_skills"]) == 0
    assert len(result["matched_skills"]) == 3
    assert result["disclaimer"] == DISCLAIMER


def test_partial_and_missing_skills():
    # Candidate knows React and Python
    candidate_skills = [
        {"id": "python", "name": "Python", "verified": True},
        {"id": "react", "name": "React", "verified": True},
    ]

    # Job requires Python (Mandatory), Next.js (Mandatory), and Kubernetes (Preferred)
    job_skills = [
        {"id": "python", "name": "Python", "is_mandatory": True, "weight": 2.0},
        {"id": "nextjs", "name": "Next.js", "is_mandatory": True, "weight": 2.0},
        {"id": "kubernetes", "name": "Kubernetes", "is_mandatory": False, "weight": 2.0},
    ]

    result = compute_compatibility_score(
        candidate_skills=candidate_skills,
        job_skills=job_skills,
        candidate_experience_years=2.0,
        required_experience_years=4.0,
    )

    # Next.js should be partially matched via React
    assert len(result["matched_skills"]) == 1  # Python
    assert len(result["partially_matched_skills"]) == 1  # Next.js (via React)
    assert len(result["missing_preferred_skills"]) == 1  # Kubernetes
    assert result["overall_score"] < 100.0
    assert result["overall_score"] > 30.0
