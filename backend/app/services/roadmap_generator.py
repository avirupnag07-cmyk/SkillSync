"""Personalized Learning Roadmap and Recommendation Generation Engine.

Generates structured, time-sequenced weekly learning plans mapped to missing skill gaps,
incorporating verified free courses, official documentation, and milestone project deliverables.
"""

from typing import Dict, List, Optional
from app.services.skill_taxonomy import CATEGORIES, SKILL_TAXONOMY, get_skill_metadata


# Hierarchy ordering for learning prerequisites
CATEGORY_PRIORITY = {
    "languages": 1,
    "frameworks_libraries": 2,
    "databases_data": 3,
    "cloud_devops": 4,
    "ai_ml": 5,
    "developer_tools": 6,
    "soft_skills": 7,
    "certifications": 8,
}


def generate_learning_roadmap(
    missing_skills: List[dict],
    target_role_title: str = "Target Engineering Role",
    duration_weeks: int = 6
) -> dict:
    """Generate an adaptive, weekly learning roadmap targeting identified skill gaps."""
    if not missing_skills:
        return {
            "title": f"Skill Mastery Plan: {target_role_title}",
            "duration_weeks": 2,
            "total_skills": 0,
            "weeks": [
                {
                    "week_number": 1,
                    "title": "Portfolio Refinement & Architectural Deep Dive",
                    "goal": "Strengthen existing competencies through system design writeups and open-source contributions.",
                    "skills": [],
                    "documentation_links": ["https://github.com/donnemartin/system-design-primer"],
                    "free_resources": ["System Design Primer", "Google Engineering Practices"],
                    "project_milestone": "Publish an architectural case study of a past project highlighting scalability trade-offs.",
                    "tasks": [
                        {"id": "w1-t1", "description": "Write a detailed README and ADR for your flagship project", "completed": False},
                        {"id": "w1-t2", "description": "Conduct mock system design interviews focusing on distributed caching and concurrency", "completed": False}
                    ]
                }
            ]
        }

    # Sort skills by pedagogical sequence (languages -> frameworks -> data -> devops -> ai)
    sorted_skills = sorted(
        missing_skills,
        key=lambda s: (
            0 if s.get("is_mandatory", True) else 1,
            CATEGORY_PRIORITY.get(s.get("category", "languages"), 9),
            -float(s.get("weight", 1.0))
        )
    )

    # Distribute skills across weeks
    actual_weeks = max(3, min(duration_weeks, len(sorted_skills) * 2))
    weeks = []

    # Partition skills evenly across the weeks
    skills_per_week = max(1, round(len(sorted_skills) / actual_weeks + 0.49))
    
    current_skill_idx = 0
    total_skills_count = len(sorted_skills)

    for w in range(1, actual_weeks + 1):
        week_skills = []
        for _ in range(skills_per_week):
            if current_skill_idx < total_skills_count:
                week_skills.append(sorted_skills[current_skill_idx])
                current_skill_idx += 1

        if not week_skills and w > 1:
            # Final capstone week
            weeks.append({
                "week_number": w,
                "title": f"Capstone Integration & System Verification",
                "goal": f"Synthesize all acquired skills into a unified, deployable open-source demonstration for {target_role_title}.",
                "skills": [{"name": s.get("name", s.get("id"))} for s in sorted_skills[:4]],
                "documentation_links": ["https://12factor.net/"],
                "free_resources": ["The Twelve-Factor App Methodology", "GitHub Actions Documentation"],
                "project_milestone": "Deploy a complete multi-tier microservice with automated CI/CD and comprehensive monitoring.",
                "tasks": [
                    {"id": f"w{w}-t1", "description": "Instrument continuous deployment with automated health check alerts", "completed": False},
                    {"id": f"w{w}-t2", "description": "Document complete architecture diagram and technical benchmark report", "completed": False}
                ]
            })
            break

        skill_names = [s.get("name", s.get("id")) for s in week_skills]
        week_title = f"Phase {w}: " + " & ".join(skill_names[:2])
        if len(skill_names) > 2:
            week_title += f" (+{len(skill_names)-2} more)"

        doc_links = []
        free_res = []
        project_ideas = []

        for s in week_skills:
            meta = get_skill_metadata(s.get("id", "")) or s
            if meta.get("docs_url"):
                doc_links.append(meta["docs_url"])
            if meta.get("free_courses"):
                free_res.extend(meta["free_courses"])
            if meta.get("project_idea"):
                project_ideas.append(meta["project_idea"])

        primary_project = project_ideas[0] if project_ideas else (
            f"Build a standalone working POC demonstrating proficiency in {', '.join(skill_names)}."
        )

        tasks = []
        for idx, s_name in enumerate(skill_names):
            tasks.append({
                "id": f"w{w}-t{idx*2+1}",
                "description": f"Complete core syntax and architectural patterns for {s_name}",
                "completed": False
            })
            tasks.append({
                "id": f"w{w}-t{idx*2+2}",
                "description": f"Implement and unit-test practical module using {s_name}",
                "completed": False
            })

        weeks.append({
            "week_number": w,
            "title": week_title,
            "goal": f"Master practical fundamentals and production best practices for {', '.join(skill_names)}.",
            "skills": week_skills,
            "documentation_links": list(dict.fromkeys(doc_links)),
            "free_resources": list(dict.fromkeys(free_res))[:3],
            "project_milestone": primary_project,
            "tasks": tasks
        })

    return {
        "title": f"Targeted Skill Bridge: {target_role_title}",
        "duration_weeks": len(weeks),
        "total_skills": len(sorted_skills),
        "target_role": target_role_title,
        "weeks": weeks
    }
