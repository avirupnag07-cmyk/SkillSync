"""Unit tests for market intelligence and role comparison services."""

from app.services.market_analyzer import compute_market_skill_demand, compare_engineering_roles


def test_market_demand_analysis():
    data = compute_market_skill_demand()
    assert data["total_jobs_analyzed"] >= 4
    assert len(data["top_skills"]) > 5
    assert len(data["category_distribution"]) > 0
    # Top skills should contain common tech skills
    skill_names = [s["name"] for s in data["top_skills"]]
    assert any("Python" in name for name in skill_names)


def test_role_comparison():
    res = compare_engineering_roles("ai_engineer", "data_scientist")
    assert res["role_a"]["title"] == "AI / Machine Learning Engineer"
    assert res["role_b"]["title"] == "Data Scientist"
    assert len(res["shared_skills"]) > 0
    assert len(res["role_a"]["unique_skills"]) > 0
    assert len(res["role_b"]["unique_skills"]) > 0
    assert 0.0 <= res["overlap_percentage"] <= 100.0
    assert 0.0 <= res["transition_difficulty_score"] <= 100.0
