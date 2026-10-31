"""Market Intelligence and Cross-Role Career Analytics Engine.

Aggregates real-time demand frequencies across postings, computes skill prevalence rankings,
salary correlations, and cross-role competency overlap matrices (e.g., AI Engineer vs. Data Scientist).
"""

from typing import Dict, List, Optional, Set
from app.services.skill_taxonomy import CATEGORIES, SKILL_TAXONOMY, get_skill_metadata
from app.services.job_api_service import CURATED_BENCHMARK_JOBS, search_all_jobs


ROLE_TAXONOMY = {
    "ai_engineer": {
        "title": "AI / Machine Learning Engineer",
        "description": "Designs, trains, and deploys production AI agents, LLM pipelines, and deep neural architectures.",
        "core_skills": ["python", "pytorch", "huggingface", "llms", "rag", "vector_databases", "docker", "fastapi", "mlops"],
        "average_salary": "$165,000",
        "demand_trend": "+42% YoY",
    },
    "data_scientist": {
        "title": "Data Scientist",
        "description": "Applies statistical modeling, predictive algorithms, and experimental design to extract strategic insights.",
        "core_skills": ["python", "r", "sql", "scikit_learn", "pandas", "numpy", "data_warehousing", "problem_solving"],
        "average_salary": "$145,000",
        "demand_trend": "+18% YoY",
    },
    "data_engineer": {
        "title": "Data Engineer",
        "description": "Builds high-throughput distributed pipelines, data lakes, and dimensional warehouses for analytics.",
        "core_skills": ["python", "sql", "apache_spark", "apache_kafka", "snowflake", "bigquery", "data_warehousing", "postgresql"],
        "average_salary": "$152,000",
        "demand_trend": "+26% YoY",
    },
    "fullstack_engineer": {
        "title": "Full Stack Engineer",
        "description": "Develops end-to-end web applications across modern user interfaces, backend APIs, and persistence layers.",
        "core_skills": ["typescript", "javascript", "react", "nextjs", "python", "fastapi", "postgresql", "tailwind", "docker"],
        "average_salary": "$140,000",
        "demand_trend": "+22% YoY",
    },
    "devops_cloud": {
        "title": "DevOps & Cloud Engineer",
        "description": "Architects resilient cloud infrastructure, automated CI/CD deployment pipelines, and observability.",
        "core_skills": ["aws", "gcp", "docker", "kubernetes", "terraform", "ci_cd", "linux", "bash", "system_design"],
        "average_salary": "$155,000",
        "demand_trend": "+28% YoY",
    }
}


def compute_market_skill_demand(jobs: Optional[List[dict]] = None) -> dict:
    """Analyze job postings to extract market-wide skill frequency rankings and category shares."""
    if not jobs:
        jobs = search_all_jobs(query="")

    skill_counts: Dict[str, int] = {}
    mandatory_counts: Dict[str, int] = {}
    total_postings = len(jobs) or 1

    category_counts: Dict[str, int] = {c: 0 for c in CATEGORIES.keys()}

    for job in jobs:
        extracted = job.get("extracted_skills", [])
        seen_in_job: Set[str] = set()

        for s in extracted:
            s_id = s["id"]
            if s_id in seen_in_job:
                continue
            seen_in_job.add(s_id)

            skill_counts[s_id] = skill_counts.get(s_id, 0) + 1
            if s.get("is_mandatory", True):
                mandatory_counts[s_id] = mandatory_counts.get(s_id, 0) + 1

            cat = s.get("category", "languages")
            if cat in category_counts:
                category_counts[cat] += 1

    # Format top ranked skills
    ranked_skills = []
    for s_id, count in sorted(skill_counts.items(), key=lambda item: item[1], reverse=True):
        meta = get_skill_metadata(s_id) or {}
        pct = round((count / total_postings) * 100.0, 1)
        ranked_skills.append({
            "id": s_id,
            "name": meta.get("name", s_id),
            "category": meta.get("category", "languages"),
            "category_name": CATEGORIES.get(meta.get("category", ""), "Other"),
            "frequency": count,
            "demand_percentage": pct,
            "mandatory_ratio": round((mandatory_counts.get(s_id, 0) / count) * 100.0, 1) if count else 0.0,
            "weight": meta.get("weight", 1.5)
        })

    # Category distribution for pie / donut charts
    total_cat_instances = sum(category_counts.values()) or 1
    category_distribution = []
    for cat_id, cnt in category_counts.items():
        category_distribution.append({
            "category_id": cat_id,
            "name": CATEGORIES.get(cat_id, cat_id),
            "count": cnt,
            "percentage": round((cnt / total_cat_instances) * 100.0, 1)
        })

    return {
        "total_jobs_analyzed": total_postings,
        "unique_skills_tracked": len(ranked_skills),
        "top_skills": ranked_skills[:20],
        "category_distribution": sorted(category_distribution, key=lambda c: c["count"], reverse=True),
        "emerging_technologies": [
            {"name": "LangGraph", "category": "AI Agents", "growth": "+185% YoY"},
            {"name": "RAG Architectures", "category": "AI / Retrieval", "growth": "+140% YoY"},
            {"name": "Vector Databases", "category": "Databases", "growth": "+115% YoY"},
            {"name": "Next.js App Router", "category": "Web Frameworks", "growth": "+65% YoY"},
            {"name": "Rust Systems", "category": "Languages", "growth": "+55% YoY"},
        ]
    }


def compare_engineering_roles(role_a_key: str, role_b_key: str) -> dict:
    """Compare two technical career tracks, revealing shared core vs. specialized requirements."""
    role_a = ROLE_TAXONOMY.get(role_a_key, ROLE_TAXONOMY["ai_engineer"])
    role_b = ROLE_TAXONOMY.get(role_b_key, ROLE_TAXONOMY["data_scientist"])

    set_a = set(role_a["core_skills"])
    set_b = set(role_b["core_skills"])

    shared = set_a.intersection(set_b)
    unique_a = set_a.difference(set_b)
    unique_b = set_b.difference(set_a)

    def format_skills(id_set: Set[str]) -> List[dict]:
        res = []
        for s_id in id_set:
            meta = get_skill_metadata(s_id) or {"name": s_id, "category": "languages"}
            res.append({
                "id": s_id,
                "name": meta["name"],
                "category": meta.get("category", "languages"),
                "category_name": CATEGORIES.get(meta.get("category", ""), "Other")
            })
        return sorted(res, key=lambda x: x["name"])

    # Overlap / Transition difficulty calculation
    overlap_pct = round((len(shared) / max(len(set_a), len(set_b))) * 100.0, 1)
    transition_delta = round(100.0 - overlap_pct, 1)

    return {
        "role_a": {
            "key": role_a_key,
            "title": role_a["title"],
            "description": role_a["description"],
            "average_salary": role_a["average_salary"],
            "demand_trend": role_a["demand_trend"],
            "total_core_skills": len(set_a),
            "unique_skills": format_skills(unique_a)
        },
        "role_b": {
            "key": role_b_key,
            "title": role_b["title"],
            "description": role_b["description"],
            "average_salary": role_b["average_salary"],
            "demand_trend": role_b["demand_trend"],
            "total_core_skills": len(set_b),
            "unique_skills": format_skills(unique_b)
        },
        "shared_skills": format_skills(shared),
        "overlap_percentage": overlap_pct,
        "transition_difficulty_score": transition_delta,
        "recommendation": (
            f"Transitioning from {role_a['title']} to {role_b['title']} has an estimated {overlap_pct}% capability overlap. "
            f"Focus your learning roadmap primarily on: {', '.join([s['name'] for s in format_skills(unique_b)[:3]])}."
        )
    }
