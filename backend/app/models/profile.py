"""Candidate Profile and Structured Competency SQLAlchemy Model."""

import datetime
from sqlalchemy import Column, String, Float, DateTime, Text
from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(64), nullable=True)
    linkedin = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    experience_years = Column(Float, default=2.0)
    bio = Column(Text, nullable=True)
    raw_resume_text = Column(Text, nullable=True)

    # JSON-encoded structures
    skills_json = Column(Text, default="[]")
    experiences_json = Column(Text, default="[]")
    projects_json = Column(Text, default="[]")
    education_json = Column(Text, default="[]")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
