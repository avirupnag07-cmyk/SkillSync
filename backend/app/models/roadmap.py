"""Personalized Learning Roadmap Persistence SQLAlchemy Model."""

import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from app.core.database import Base


class SavedRoadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=True)
    gap_analysis_id = Column(String(64), index=True, nullable=True)
    title = Column(String(255), nullable=False)
    target_role = Column(String(255), nullable=False)
    duration_weeks = Column(Integer, default=6)
    roadmap_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
