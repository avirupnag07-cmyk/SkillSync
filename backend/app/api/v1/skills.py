"""Skill Taxonomy, Extraction, and Normalization API Routes."""

from typing import Dict, List
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.skill_taxonomy import (
    CATEGORIES,
    SKILL_TAXONOMY,
    get_all_canonical_skills,
    get_skill_metadata,
    normalize_skill_name,
)
from app.services.skill_extractor import extract_skills_from_text

router = APIRouter(prefix="/skills", tags=["Skill Taxonomy"])


class SkillExtractRequest(BaseModel):
    text: str
    is_job_posting: bool = False


class NormalizeRequest(BaseModel):
    raw_name: str


@router.get("/taxonomy")
def get_taxonomy_catalog():
    """Retrieve full skill catalog grouped by technical domain."""
    skills = get_all_canonical_skills()
    grouped: Dict[str, list] = {k: [] for k in CATEGORIES.keys()}
    for s in skills:
        cat = s.get("category", "languages")
        if cat in grouped:
            grouped[cat].append(s)
    return {
        "categories": CATEGORIES,
        "total_skills": len(skills),
        "grouped_skills": grouped
    }


@router.post("/extract")
def extract_skills_endpoint(payload: SkillExtractRequest):
    """Run real-time entity recognition and ontology normalization on raw text."""
    extracted = extract_skills_from_text(
        payload.text,
        default_mandatory=True,
        is_job_posting=payload.is_job_posting
    )
    return {
        "skills_count": len(extracted),
        "skills": extracted
    }


@router.post("/normalize")
def normalize_skill_endpoint(payload: NormalizeRequest):
    """Normalize raw colloquial name (e.g. 'JS' -> 'JavaScript') with metadata."""
    canon_id = normalize_skill_name(payload.raw_name)
    if not canon_id:
        return {"raw_name": payload.raw_name, "canonical_id": None, "metadata": None}
    meta = get_skill_metadata(canon_id)
    return {
        "raw_name": payload.raw_name,
        "canonical_id": canon_id,
        "metadata": meta
    }
