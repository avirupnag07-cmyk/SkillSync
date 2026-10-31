"""Skill Gap Analysis and Compatibility Snapshot SQLAlchemy Model."""

import datetime
from sqlalchemy import Column, String, Float, DateTime, Text
from app.core.database import Base


class SavedGapAnalysis(Base):
    __tablename__ = "gap_analyses"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=True)
    profile_id = Column(String(64), index=True, nullable=True)
    job_id = Column(String(64), index=True, nullable=True)
    job_title = Column(String(255), nullable=True)
    candidate_name = Column(String(255), nullable=True)

    overall_score = Column(Float, nullable=False)
    mandatory_score = Column(Float, nullable=False)
    preferred_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    alignment_tier = Column(String(128), nullable=False)

    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
