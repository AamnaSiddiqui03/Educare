from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.data.models import Gender, ParentLiveStatus, ApplicantType


# Student Profile Schemas
class StudentProfileCreate(BaseModel):
    """Schema for creating student profile"""
    # Basic Profile Information
    phone: str
    address: str
    photo_url: Optional[str] = None
    video_url: Optional[str] = None
    help_text: str
    
    # Personal Information
    gender: Optional[Gender] = None
    age: Optional[int] = None
    
    # Parent/Guardian Information
    parent_guardian_occupation: Optional[str] = None
    parent_guardian_monthly_income: Optional[int] = None
    parents_education_status: Optional[str] = None
    parent_live_status: Optional[ParentLiveStatus] = None
    
    # Scholarship Information
    scholarship_amount_requested: Optional[int] = None
    is_eligible_for_zakat: Optional[bool] = None
    
    # Applicant Information
    applicant_email: Optional[str] = None
    applicant_type: Optional[ApplicantType] = None
    applicant_name: Optional[str] = None
    applicant_mobile_number: Optional[str] = None


class StudentProfileUpdate(BaseModel):
    """Schema for updating student profile"""
    # Basic Profile Information
    phone: Optional[str] = None
    address: Optional[str] = None
    photo_url: Optional[str] = None
    video_url: Optional[str] = None
    help_text: Optional[str] = None
    
    # Personal Information
    gender: Optional[Gender] = None
    age: Optional[int] = None
    
    # Parent/Guardian Information
    parent_guardian_occupation: Optional[str] = None
    parent_guardian_monthly_income: Optional[int] = None
    parents_education_status: Optional[str] = None
    parent_live_status: Optional[ParentLiveStatus] = None
    
    # Scholarship Information
    scholarship_amount_requested: Optional[int] = None
    is_eligible_for_zakat: Optional[bool] = None
    
    # Applicant Information
    applicant_email: Optional[str] = None
    applicant_type: Optional[ApplicantType] = None
    applicant_name: Optional[str] = None
    applicant_mobile_number: Optional[str] = None


class StudentProfileResponse(BaseModel):
    """Schema for student profile response"""
    student_id: str
    user_id: str
    
    # Basic Profile Information
    phone: str
    address: str
    photo_url: Optional[str]
    video_url: Optional[str]
    help_text: str
    
    # Personal Information
    gender: Optional[Gender]
    age: Optional[int]
    
    # Parent/Guardian Information
    parent_guardian_occupation: Optional[str]
    parent_guardian_monthly_income: Optional[int]
    parents_education_status: Optional[str]
    parent_live_status: Optional[ParentLiveStatus]
    
    # Scholarship Information
    scholarship_amount_requested: Optional[int]
    is_eligible_for_zakat: Optional[bool]
    
    # Applicant Information
    applicant_email: Optional[str]
    applicant_type: Optional[ApplicantType]
    applicant_name: Optional[str]
    applicant_mobile_number: Optional[str]
    
    # Status Fields
    profile_completed: bool
    assessment_completed: bool
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class StudentProgressResponse(BaseModel):
    """Schema for student progress response"""
    profile_completed: bool
    assessment_completed: bool
    message: str


# Education Schemas
class EducationCreate(BaseModel):
    """Schema for creating education entry"""
    institution_name: str
    education_level: str
    year_of_passing: str
    marks_obtained: Optional[str] = None
    report_card_url: Optional[str] = None


class EducationUpdate(BaseModel):
    """Schema for updating education entry"""
    institution_name: Optional[str] = None
    education_level: Optional[str] = None
    year_of_passing: Optional[str] = None
    marks_obtained: Optional[str] = None
    report_card_url: Optional[str] = None


class EducationResponse(BaseModel):
    """Schema for education entry response"""
    education_id: str
    student_id: str
    institution_name: str
    education_level: str
    year_of_passing: str
    marks_obtained: Optional[str]
    report_card_url: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


# Assessment Schemas
class AssessmentStartResponse(BaseModel):
    """Schema for assessment start response"""
    assessment_id: str
    assessment_name: str
    assessment_type: str
    description: Optional[str]
    total_questions: str
    time_limit_minutes: str
    questions: dict  # JSON questions from external source


class AssessmentSubmit(BaseModel):
    """Schema for assessment submission"""
    answers: dict  # JSON answers from frontend


class AssessmentSubmitResponse(BaseModel):
    """Schema for assessment submission response"""
    submission_id: str
    assessment_completed: bool
    report_pdf_url: Optional[str]
    message: str


class AssessmentReportResponse(BaseModel):
    """Schema for assessment report response"""
    submission_id: str
    assessment_name: str
    report_pdf_url: str
    submitted_at: str


# Base Response Schemas
class StudentBaseResponse(BaseModel):
    """Base response schema for student operations"""
    success: bool = True
    message: str


class StudentErrorResponse(BaseModel):
    """Error response schema for student operations"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
