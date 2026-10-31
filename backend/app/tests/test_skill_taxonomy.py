"""Unit tests for skill taxonomy, normalization, and similarity relationships."""

from app.services.skill_taxonomy import (
    normalize_skill_name,
    get_skill_metadata,
    calculate_skill_similarity,
    SKILL_TAXONOMY,
)


def test_alias_normalization():
    assert normalize_skill_name("js") == "javascript"
    assert normalize_skill_name("JavaScript") == "javascript"
    assert normalize_skill_name("TS") == "typescript"
    assert normalize_skill_name("py") == "python"
    assert normalize_skill_name("k8s") == "kubernetes"
    assert normalize_skill_name("postgres") == "postgresql"
    assert normalize_skill_name("psql") == "postgresql"
    assert normalize_skill_name("reactjs") == "react"
    assert normalize_skill_name("next.js") == "nextjs"
    assert normalize_skill_name("tf") == "tensorflow"
    assert normalize_skill_name("sklearn") == "scikit_learn"


def test_skill_metadata_retrieval():
    meta = get_skill_metadata("python")
    assert meta is not None
    assert meta["name"] == "Python"
    assert meta["category"] == "languages"
    assert meta["weight"] >= 1.5
    assert "docs_url" in meta
    assert len(meta.get("free_courses", [])) > 0


def test_skill_similarity():
    # Identical skill
    assert calculate_skill_similarity("python", "python") == 1.0

    # Explicitly related skills
    sim_react_next = calculate_skill_similarity("react", "nextjs")
    assert sim_react_next >= 0.8

    sim_torch_tf = calculate_skill_similarity("pytorch", "tensorflow")
    assert sim_torch_tf >= 0.7

    # Same category bonus (e.g. languages)
    sim_go_java = calculate_skill_similarity("go", "java")
    assert sim_go_java >= 0.2

    # Unrelated skills across different categories
    sim_unrelated = calculate_skill_similarity("react", "problem_solving")
    assert sim_unrelated == 0.0
