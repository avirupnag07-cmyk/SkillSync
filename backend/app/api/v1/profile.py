"""Career Profile and Resume Processing API Routes."""

import json
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_optional
from app.models.profile import Profile
from app.schemas.profile import ProfileCreateOrUpdate, ProfileOut
from app.services.resume_parser import parse_resume_document
from app.services.skill_taxonomy import get_skill_metadata, normalize_skill_name

router = APIRouter(prefix="/profile", tags=["Career Profile"])


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_optional)
):
    """Parse PDF, DOCX, or text resume, extract competencies, and initialize candidate profile."""
    content = await file.read()
    filename = file.filename or "resume.pdf"

    if not filename.lower().endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported format. Please upload a PDF (.pdf), Word Document (.docx), or plain text (.txt)."
        )

    parsed = parse_resume_document(content, filename)

    # Automatically persist or update candidate profile
    profile_id = f"prof-{uuid.uuid4().hex[:10]}"
    new_profile = Profile(
        id=profile_id,
        user_id=user["sub"],
        name=parsed["name"],
        email=parsed["email"],
        phone=parsed["phone"],
        linkedin=parsed["linkedin"],
        github=parsed["github"],
        experience_years=parsed["estimated_experience_years"],
        raw_resume_text=parsed["raw_text"],
        skills_json=json.dumps(parsed["skills"]),
        experiences_json=json.dumps([]),
        projects_json=json.dumps([]),
        education_json=json.dumps([])
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "profile_id": new_profile.id,
        "name": new_profile.name,
        "email": new_profile.email,
        "phone": new_profile.phone,
        "linkedin": new_profile.linkedin,
        "github": new_profile.github,
        "experience_years": new_profile.experience_years,
        "extracted_skills": parsed["skills"],
        "skills_count": len(parsed["skills"]),
        "message": "Resume successfully analyzed and structured profile created."
    }


@router.post("/save")
def save_profile(
    profile_data: ProfileCreateOrUpdate,
    profile_id: Optional[str] = None,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_optional)
):
    """Create or manually update structured candidate profile details."""
    p_id = profile_id or f"prof-{uuid.uuid4().hex[:10]}"
    existing = db.query(Profile).filter(Profile.id == p_id).first()

    skills_dict_list = [s.model_dump() for s in profile_data.skills]
    exp_dict_list = [e.model_dump() for e in profile_data.experiences]
    proj_dict_list = [p.model_dump() for p in profile_data.projects]
    edu_dict_list = [ed.model_dump() for ed in profile_data.education]

    if existing:
        existing.name = profile_data.name
        existing.email = profile_data.email
        existing.phone = profile_data.phone
        existing.linkedin = profile_data.linkedin
        existing.github = profile_data.github
        existing.experience_years = profile_data.experience_years
        existing.bio = profile_data.bio
        existing.skills_json = json.dumps(skills_dict_list)
        existing.experiences_json = json.dumps(exp_dict_list)
        existing.projects_json = json.dumps(proj_dict_list)
        existing.education_json = json.dumps(edu_dict_list)
        target_profile = existing
    else:
        target_profile = Profile(
            id=p_id,
            user_id=user["sub"],
            name=profile_data.name,
            email=profile_data.email,
            phone=profile_data.phone,
            linkedin=profile_data.linkedin,
            github=profile_data.github,
            experience_years=profile_data.experience_years,
            bio=profile_data.bio,
            skills_json=json.dumps(skills_dict_list),
            experiences_json=json.dumps(exp_dict_list),
            projects_json=json.dumps(proj_dict_list),
            education_json=json.dumps(edu_dict_list)
        )
        db.add(target_profile)

    db.commit()
    db.refresh(target_profile)

    return {
        "status": "success",
        "profile_id": target_profile.id,
        "message": "Profile saved successfully."
    }


@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    """Retrieve candidate profile by ID."""
    p = db.query(Profile).filter(Profile.id == profile_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found.")

    return ProfileOut(
        id=p.id,
        user_id=p.user_id,
        name=p.name,
        email=p.email,
        phone=p.phone,
        linkedin=p.linkedin,
        github=p.github,
        experience_years=p.experience_years,
        bio=p.bio,
        skills=json.loads(p.skills_json or "[]"),
        experiences=json.loads(p.experiences_json or "[]"),
        projects=json.loads(p.projects_json or "[]"),
        education=json.loads(p.education_json or "[]"),
        created_at=p.created_at.isoformat() if p.created_at else None
    )


@router.post("/{profile_id}/add-skill")
def add_skill_to_profile(profile_id: str, skill_name: str, db: Session = Depends(get_db)):
    """Add a verified or custom skill to a candidate's profile."""
    p = db.query(Profile).filter(Profile.id == profile_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found.")

    skills = json.loads(p.skills_json or "[]")
    canon_id = normalize_skill_name(skill_name) or skill_name.strip().lower()
    meta = get_skill_metadata(canon_id)

    # Avoid duplicates
    if not any(s.get("id") == canon_id for s in skills):
        skills.append({
            "id": canon_id,
            "name": meta["name"] if meta else skill_name,
            "category": meta["category"] if meta else "languages",
            "weight": meta["weight"] if meta else 1.5,
            "verified": True
        })
        p.skills_json = json.dumps(skills)
        db.commit()

    return {"status": "success", "skills": skills}


@router.delete("/{profile_id}/remove-skill/{skill_id}")
def remove_skill_from_profile(profile_id: str, skill_id: str, db: Session = Depends(get_db)):
    """Remove a skill from a candidate's profile."""
    p = db.query(Profile).filter(Profile.id == profile_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found.")

    skills = json.loads(p.skills_json or "[]")
    updated_skills = [s for s in skills if s.get("id") != skill_id]
    p.skills_json = json.dumps(updated_skills)
    db.commit()

    return {"status": "success", "skills": updated_skills}
