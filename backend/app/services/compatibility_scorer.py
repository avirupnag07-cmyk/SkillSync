"""Explainable Career Compatibility Scoring and Gap Analysis Engine.

Implements multi-tiered weighted scoring across mandatory vs. preferred requirements,
experience alignment ratios, semantic transferable skill coefficients, and transparent explainability metrics.
"""

from typing import Dict, List, Optional, Set, Tuple
from app.services.skill_taxonomy import (
    CATEGORIES,
    SKILL_TAXONOMY,
    calculate_skill_similarity,
    get_skill_metadata,
)

DISCLAIMER = (
    "SkillSync compatibility scores evaluate semantic alignment between profile capabilities "
    "and documented job specifications. This metric is designed for learning and skills development "
    "and does not represent a guarantee of employment, interviews, or hiring outcomes."
)


def compute_compatibility_score(
    candidate_skills: List[dict],
    job_skills: List[dict],
    candidate_experience_years: float = 0.0,
    required_experience_years: float = 0.0,
) -> dict:
    """Compute deterministic, explainable compatibility score between candidate and job posting.
    
    Args:
        candidate_skills: List of candidate skills, each with at least 'id', and optionally 'years', 'verified'
        job_skills: List of extracted job skills with 'id', 'is_mandatory', 'weight', 'years_required'
        candidate_experience_years: Total candidate experience years
        required_experience_years: Experience required by job posting
    """
    candidate_ids = {s["id"]: s for s in candidate_skills}

    matched_skills = []
    partially_matched_skills = []
    missing_mandatory_skills = []
    missing_preferred_skills = []
    unverified_skills = []

    # Check unverified candidate skills (skills marked unverified or with 0 evidence)
    for c_skill in candidate_skills:
        if not c_skill.get("verified", True):
            unverified_skills.append({
                "id": c_skill["id"],
                "name": c_skill.get("name", c_skill["id"]),
                "reason": "Self-reported without verified project or employment attribution"
            })

    mandatory_total_weight = 0.0
    mandatory_earned_weight = 0.0

    preferred_total_weight = 0.0
    preferred_earned_weight = 0.0

    # Categorical breakdown trackers
    category_scores: Dict[str, dict] = {
        cat_id: {"name": cat_name, "required": 0, "matched": 0, "score": 100.0}
        for cat_id, cat_name in CATEGORIES.items()
    }

    for j_skill in job_skills:
        j_id = j_skill["id"]
        is_mand = j_skill.get("is_mandatory", True)
        weight = float(j_skill.get("weight", 1.5))
        category = j_skill.get("category", "languages")

        if category in category_scores:
            category_scores[category]["required"] += 1

        # Check for best match among candidate skills
        best_sim = 0.0
        best_match_candidate = None

        if j_id in candidate_ids:
            best_sim = 1.0
            best_match_candidate = candidate_ids[j_id]
        else:
            # Check related skills
            for c_id, c_data in candidate_ids.items():
                sim = calculate_skill_similarity(j_id, c_id)
                if sim > best_sim:
                    best_sim = sim
                    best_match_candidate = c_data

        # Update weighted scoring
        if is_mand:
            mandatory_total_weight += weight
            mandatory_earned_weight += weight * best_sim
        else:
            preferred_total_weight += weight
            preferred_earned_weight += weight * best_sim

        # Categorize the match
        skill_info = {
            "id": j_id,
            "name": j_skill.get("name", j_id),
            "category": category,
            "category_name": CATEGORIES.get(category, category),
            "is_mandatory": is_mand,
            "similarity": round(best_sim, 2),
            "weight": weight,
            "years_required": j_skill.get("years_required"),
            "docs_url": j_skill.get("docs_url"),
            "free_courses": j_skill.get("free_courses", []),
            "project_idea": j_skill.get("project_idea"),
        }

        if best_sim >= 0.98:
            skill_info["matched_with"] = best_match_candidate.get("name", j_id)
            matched_skills.append(skill_info)
            if category in category_scores:
                category_scores[category]["matched"] += 1
        elif best_sim >= 0.5:
            skill_info["matched_with"] = best_match_candidate.get("name", "Related capability")
            skill_info["transferable_skill"] = best_match_candidate.get("name")
            partially_matched_skills.append(skill_info)
            if category in category_scores:
                category_scores[category]["matched"] += 0.5
        else:
            if is_mand:
                missing_mandatory_skills.append(skill_info)
            else:
                missing_preferred_skills.append(skill_info)

    # Calculate subcomponent scores
    mandatory_score = (
        (mandatory_earned_weight / mandatory_total_weight * 100.0)
        if mandatory_total_weight > 0
        else 100.0
    )
    preferred_score = (
        (preferred_earned_weight / preferred_total_weight * 100.0)
        if preferred_total_weight > 0
        else 100.0
    )

    # Experience alignment ratio (cap at 1.0)
    if required_experience_years > 0:
        exp_ratio = min(1.0, max(0.0, candidate_experience_years / required_experience_years))
    else:
        exp_ratio = 1.0
    experience_score = exp_ratio * 100.0

    # Overall weighted score
    overall_score = round(
        (0.60 * mandatory_score) + (0.25 * preferred_score) + (0.15 * experience_score),
        1
    )

    # Category percentages
    radar_data = []
    for cat_id, cat_info in category_scores.items():
        if cat_info["required"] > 0:
            cat_pct = round((cat_info["matched"] / cat_info["required"]) * 100.0, 1)
        else:
            cat_pct = 100.0 if len(candidate_skills) > 0 else 0.0
        cat_info["score"] = cat_pct
        radar_data.append({
            "category": cat_id,
            "category_name": cat_info["name"],
            "score": cat_pct,
            "required_count": cat_info["required"],
            "matched_count": cat_info["matched"]
        })

    # Alignment tier classification
    if overall_score >= 85:
        tier = "High Alignment"
        summary = "Outstanding fit. Candidate strongly aligns with core architecture and tech stack requirements."
    elif overall_score >= 70:
        tier = "Strong Contender with Addressable Gaps"
        summary = "Competitive profile. Meets essential foundations with minor high-leverage skill gaps to bridge."
    elif overall_score >= 50:
        tier = "Moderate Alignment"
        summary = "Partial requirement coverage. Key foundational skills present, but several core technologies missing."
    else:
        tier = "Requires Structured Upskilling"
        summary = "Substantial gap between current capabilities and job requirements. Dedicated learning roadmap advised."

    return {
        "overall_score": overall_score,
        "mandatory_score": round(mandatory_score, 1),
        "preferred_score": round(preferred_score, 1),
        "experience_score": round(experience_score, 1),
        "alignment_tier": tier,
        "executive_summary": summary,
        "disclaimer": DISCLAIMER,
        "counts": {
            "total_job_skills": len(job_skills),
            "matched_count": len(matched_skills),
            "partially_matched_count": len(partially_matched_skills),
            "missing_mandatory_count": len(missing_mandatory_skills),
            "missing_preferred_count": len(missing_preferred_skills),
            "unverified_count": len(unverified_skills),
        },
        "matched_skills": matched_skills,
        "partially_matched_skills": partially_matched_skills,
        "missing_mandatory_skills": missing_mandatory_skills,
        "missing_preferred_skills": missing_preferred_skills,
        "unverified_skills": unverified_skills,
        "category_breakdown": radar_data,
    }
