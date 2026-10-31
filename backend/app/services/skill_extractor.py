"""Skill Extraction, Requirement Classification, and Contextual Analysis Engine.

Performs robust regex and heuristic NER extraction against job postings and resumes,
classifying requirements into mandatory vs. preferred tiers and parsing required experience.
"""

import re
from typing import Dict, List, Optional, Set, Tuple
from app.services.skill_taxonomy import (
    ALIAS_MAP,
    SKILL_TAXONOMY,
    get_skill_metadata,
    normalize_skill_name,
)

# Section classification headers
MANDATORY_PATTERNS = [
    r"minimum qualifications?",
    r"basic qualifications?",
    r"must have",
    r"required qualifications?",
    r"what you need",
    r"what we are looking for",
    r"core requirements?",
    r"essential skills?",
    r"technical requirements?",
    r"requirements",
]

PREFERRED_PATTERNS = [
    r"preferred qualifications?",
    r"nice to have",
    r"bonus points?",
    r"plus points?",
    r"desired skills?",
    r"good to have",
    r"it's a plus",
    r"preferred experience",
    r"extra credit",
]

# Build compiled search patterns for aliases and canonical names
# Sort keys by length descending to match longest phrases first (e.g., "Google Cloud Platform" before "Google")
SORTED_TERMS = sorted(ALIAS_MAP.keys(), key=lambda t: len(t), reverse=True)

# Build regex pattern cache
COMPILED_PATTERNS: List[Tuple[str, re.Pattern]] = []

for term in SORTED_TERMS:
    escaped = re.escape(term)
    # Special treatment for short words like 'c', 'r', 'go', 'js', 'ts' to avoid substring matches
    if len(term) <= 2:
        pattern = re.compile(rf"(?<![a-zA-Z0-9_\+\#\.\/]){escaped}(?![a-zA-Z0-9_\+\#\.\/])", re.IGNORECASE)
    else:
        pattern = re.compile(rf"\b{escaped}\b", re.IGNORECASE)
    COMPILED_PATTERNS.append((term, pattern))


def split_sections(text: str) -> List[Tuple[str, str]]:
    """Split a document into titled sections to distinguish mandatory from preferred requirements."""
    lines = text.split("\n")
    sections: List[Tuple[str, str]] = []
    
    current_title = "general"
    current_lines: List[str] = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        lower_line = stripped.lower()
        matched_section = None
        
        # Check if line looks like a header (short, ended with colon, or matches keyword)
        if len(stripped) < 60:
            for pat in PREFERRED_PATTERNS:
                if re.search(pat, lower_line):
                    matched_section = "preferred"
                    break
            if not matched_section:
                for pat in MANDATORY_PATTERNS:
                    if re.search(pat, lower_line):
                        matched_section = "mandatory"
                        break
                        
        if matched_section:
            if current_lines:
                sections.append((current_title, "\n".join(current_lines)))
                current_lines = []
            current_title = matched_section
            # Check if there is content after colon on the same line
            if ":" in stripped:
                remainder = stripped.split(":", 1)[1].strip()
                if remainder:
                    current_lines.append(remainder)
        else:
            current_lines.append(stripped)
            
    if current_lines:
        sections.append((current_title, "\n".join(current_lines)))
        
    if not sections and text.strip():
        sections.append(("mandatory", text))

    return sections


def extract_years_of_experience(text: str, skill_term: str) -> Optional[int]:
    """Extract years of experience required for a specific skill near its occurrence."""
    # Pattern e.g. "3+ years of experience in Python" or "Python (3-5 years)"
    escaped = re.escape(skill_term)
    patterns = [
        rf"(\d+)\+?\s*(?:-\s*\d+)?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience)?(?:\s+in|\s+with|\s+using)?\s+{escaped}",
        rf"{escaped}[^\.\n]{{0,35}}?(\d+)\+?\s*(?:-\s*\d+)?\s*(?:years?|yrs?)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except (ValueError, IndexError):
                pass
    return None


def extract_skills_from_text(
    text: str,
    default_mandatory: bool = True,
    is_job_posting: bool = False
) -> List[dict]:
    """Extract and normalize all skills found within text.
    
    If is_job_posting is True, automatically parses document sections into
    mandatory and preferred tiers.
    """
    if not text:
        return []

    sections = split_sections(text) if is_job_posting else [("general", text)]
    
    extracted: Dict[str, dict] = {}

    for section_type, section_content in sections:
        # Determine requirement tier
        is_mandatory = default_mandatory
        if section_type == "preferred":
            is_mandatory = False
        elif section_type == "mandatory":
            is_mandatory = True

        for term, pattern in COMPILED_PATTERNS:
            matches = list(pattern.finditer(section_content))
            if not matches:
                continue

            canonical_id = ALIAS_MAP.get(term)
            if not canonical_id or canonical_id not in SKILL_TAXONOMY:
                continue

            meta = SKILL_TAXONOMY[canonical_id]
            years_req = extract_years_of_experience(section_content, term)

            if canonical_id not in extracted:
                extracted[canonical_id] = {
                    "id": canonical_id,
                    "name": meta["name"],
                    "category": meta["category"],
                    "weight": meta["weight"],
                    "is_mandatory": is_mandatory,
                    "years_required": years_req,
                    "matched_terms": [term],
                    "mention_count": len(matches),
                    "docs_url": meta.get("docs_url"),
                    "free_courses": meta.get("free_courses", []),
                    "project_idea": meta.get("project_idea")
                }
            else:
                # If seen in a mandatory section previously, retain mandatory
                if is_mandatory:
                    extracted[canonical_id]["is_mandatory"] = True
                if term not in extracted[canonical_id]["matched_terms"]:
                    extracted[canonical_id]["matched_terms"].append(term)
                extracted[canonical_id]["mention_count"] += len(matches)
                if years_req and not extracted[canonical_id]["years_required"]:
                    extracted[canonical_id]["years_required"] = years_req

    return list(extracted.values())
