"""Job Posting and Extracted Specifications SQLAlchemy Model."""

import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from app.core.database import Base


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(String(64), primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    source = Column(String(64), default="manual_paste")
    salary_range = Column(String(128), nullable=True)
    required_experience_years = Column(Integer, default=3)
    description = Column(Text, nullable=False)
    skills_json = Column(Text, default="[]")
    url = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
