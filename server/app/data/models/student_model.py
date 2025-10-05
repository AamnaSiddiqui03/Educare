from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.data.db import Base


class Student(Base):
    """Student model for Phase 2 - Extended student profile"""
    __tablename__ = "students"

    student_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    phone = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    photo_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    help_text = Column(Text, nullable=False)
    profile_completed = Column(Boolean, default=False, nullable=False)
    assessment_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    education_entries = relationship("StudentEducation", back_populates="student", cascade="all, delete-orphan")
    assessments = relationship("StudentAssessment", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(student_id={self.student_id}, user_id={self.user_id})>"


class StudentEducation(Base):
    """Student education entries - allows multiple educational entries per student"""
    __tablename__ = "student_education"

    education_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.student_id"), nullable=False)
    institution_name = Column(String, nullable=False)
    education_level = Column(String, nullable=False)  # Class 10, Class 12, Undergraduate, etc.
    year_of_passing = Column(String, nullable=False)  # Changed to String for flexibility
    marks_obtained = Column(String, nullable=True)    # Changed to String for flexibility
    report_card_url = Column(String, nullable=True)   # Future feature
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    student = relationship("Student", back_populates="education_entries")

    def __repr__(self):
        return f"<StudentEducation(education_id={self.education_id}, institution={self.institution_name})>"


class StudentAssessment(Base):
    """Student assessment submissions and PDF reports"""
    __tablename__ = "student_assessment"

    submission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.student_id"), nullable=False)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessment_master.assessment_id"), nullable=False)
    report_pdf_url = Column(String, nullable=True)  # Generated PDF report
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("Student", back_populates="assessments")
    assessment = relationship("AssessmentMaster", foreign_keys=[assessment_id])

    def __repr__(self):
        return f"<StudentAssessment(submission_id={self.submission_id}, student_id={self.student_id})>"
