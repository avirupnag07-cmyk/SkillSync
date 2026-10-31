"""Unit tests for PDF and CSV export generation."""

from app.services.report_generator import (
    generate_gap_csv,
    generate_gap_pdf,
    generate_roadmap_csv,
    generate_roadmap_pdf,
)

SAMPLE_GAP_DATA = {
    "overall_score": 82.5,
    "mandatory_score": 85.0,
    "preferred_score": 75.0,
    "experience_score": 80.0,
    "alignment_tier": "Strong Contender with Addressable Gaps",
    "executive_summary": "Candidate possesses strong core competencies with minor gaps.",
    "disclaimer": "SkillSync compatibility score represents semantic requirement alignment.",
    "matched_skills": [
        {"name": "Python", "category": "languages", "similarity": 1.0, "weight": 2.0}
    ],
    "partially_matched_skills": [],
    "missing_mandatory_skills": [
        {"name": "Kubernetes", "category": "cloud_devops", "weight": 2.0, "project_idea": "Deploy a K8s cluster."}
    ],
    "missing_preferred_skills": [],
    "unverified_skills": []
}

SAMPLE_ROADMAP_DATA = {
    "title": "Targeted Skill Bridge: AI Specialist",
    "duration_weeks": 4,
    "target_role": "AI Specialist",
    "weeks": [
        {
            "week_number": 1,
            "title": "Phase 1: Kubernetes Deployment",
            "goal": "Master container orchestration and ingress.",
            "skills": [{"name": "Kubernetes"}],
            "project_milestone": "Deploy microservice cluster.",
            "tasks": [
                {"id": "w1-t1", "description": "Configure ingress and TLS certs", "completed": False}
            ]
        }
    ]
}


def test_gap_csv_generation():
    csv_bytes = generate_gap_csv(SAMPLE_GAP_DATA, "Taylor Reed", "AI Specialist")
    content = csv_bytes.decode("utf-8")
    assert "SKILLSYNC - CAREER COMPATIBILITY" in content
    assert "Taylor Reed" in content
    assert "82.5%" in content
    assert "Kubernetes" in content


def test_gap_pdf_generation():
    pdf_bytes = generate_gap_pdf(SAMPLE_GAP_DATA, "Taylor Reed", "AI Specialist")
    assert len(pdf_bytes) > 200
    assert pdf_bytes.startswith(b"%PDF")


def test_roadmap_csv_generation():
    csv_bytes = generate_roadmap_csv(SAMPLE_ROADMAP_DATA)
    content = csv_bytes.decode("utf-8")
    assert "SKILLSYNC - PERSONALIZED LEARNING ROADMAP" in content
    assert "Kubernetes Deployment" in content


def test_roadmap_pdf_generation():
    pdf_bytes = generate_roadmap_pdf(SAMPLE_ROADMAP_DATA)
    assert len(pdf_bytes) > 200
    assert pdf_bytes.startswith(b"%PDF")
