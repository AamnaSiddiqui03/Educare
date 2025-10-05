from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.data.db import Base


class AssessmentMaster(Base):
    """Master table for available assessments"""
    __tablename__ = "assessment_master"

    assessment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_name = Column(String, nullable=False)
    assessment_type = Column(String, nullable=False)  # aptitude, personality, career_interest
    description = Column(Text, nullable=True)
    total_questions = Column(String, nullable=False)
    time_limit_minutes = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AssessmentMaster(assessment_id={self.assessment_id}, name={self.assessment_name})>"
