"""Unit tests for resume ingestion and candidate contact extraction."""

from app.services.resume_parser import extract_candidate_contact, parse_resume_document

SAMPLE_RESUME_TEXT = """
Alex Morgan
Senior AI Engineer
Email: alex.morgan@example.com
Phone: (555) 234-5678
LinkedIn: linkedin.com/in/alexmorgan-ai
GitHub: github.com/alexmorgan-code

Professional Summary:
Passionate AI Engineer with 4+ years of experience building production LLM agents,
RAG architectures, and scalable Python microservices.

Technical Skills:
Python, PyTorch, Transformers, LangGraph, Vector Databases, PostgreSQL, Docker, FastAPI, Git.

Experience:
Senior AI Specialist - TechCorp (2022 - Present)
- Deployed LangGraph multi-agent systems reducing inference turnaround by 40%.
"""


def test_contact_extraction():
    contact = extract_candidate_contact(SAMPLE_RESUME_TEXT)
    assert contact["email"] == "alex.morgan@example.com"
    assert "555" in contact["phone"]
    assert "linkedin.com/in/alexmorgan-ai" in contact["linkedin"]
    assert "github.com/alexmorgan-code" in contact["github"]
    assert contact["name"] == "Alex Morgan"


def test_resume_document_parsing():
    parsed = parse_resume_document(SAMPLE_RESUME_TEXT.encode("utf-8"), "alex_morgan.txt")
    assert parsed["name"] == "Alex Morgan"
    assert parsed["skills_count"] >= 6
    skill_ids = [s["id"] for s in parsed["skills"]]
    assert "python" in skill_ids
    assert "pytorch" in skill_ids
    assert "docker" in skill_ids
