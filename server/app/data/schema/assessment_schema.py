from pydantic import BaseModel
from typing import Optional, List, Dict, Any


# Assessment Master Schemas
class AssessmentMasterResponse(BaseModel):
    """Schema for assessment master response"""
    assessment_id: str
    assessment_name: str
    assessment_type: str
    description: Optional[str]
    total_questions: str
    time_limit_minutes: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True


# Assessment Start/Questions Schemas
class AssessmentStartResponse(BaseModel):
    """Schema for assessment start response"""
    assessment_id: str
    assessment_name: str
    assessment_type: str
    description: Optional[str]
    total_questions: str
    time_limit_minutes: str
    questions: Dict[str, Any]  # JSON questions from external source
    message: str = "Assessment started successfully"


# Assessment Submission Schemas
class AssessmentSubmitRequest(BaseModel):
    """Schema for assessment submission request"""
    answers: Dict[str, Any]  # JSON answers from frontend


class AssessmentSubmitResponse(BaseModel):
    """Schema for assessment submission response"""
    submission_id: str
    assessment_id: str
    assessment_name: str
    assessment_completed: bool
    report_pdf_url: Optional[str]
    submitted_at: str
    message: str


# Assessment Report Schemas
class AssessmentReportResponse(BaseModel):
    """Schema for assessment report response"""
    submission_id: str
    student_id: str
    assessment_id: str
    assessment_name: str
    report_pdf_url: Optional[str]
    submitted_at: str
    
    class Config:
        from_attributes = True


# Student Assessment History Schemas
class StudentAssessmentHistoryResponse(BaseModel):
    """Schema for student assessment history response"""
    submission_id: str
    assessment_id: str
    assessment_name: str
    assessment_type: str
    report_pdf_url: Optional[str]
    submitted_at: str
    
    class Config:
        from_attributes = True


# Assessment List Schemas
class AvailableAssessmentResponse(BaseModel):
    """Schema for available assessments response"""
    assessment_id: str
    assessment_name: str
    assessment_type: str
    description: Optional[str]
    total_questions: str
    time_limit_minutes: str
    
    class Config:
        from_attributes = True


# Base Response Schemas
class AssessmentBaseResponse(BaseModel):
    """Base response schema for assessment operations"""
    success: bool = True
    message: str


class AssessmentErrorResponse(BaseModel):
    """Error response schema for assessment operations"""
    success: bool = False
    message: str
    error_code: Optional[str] = None


# Assessment Status Schemas
class AssessmentStatusResponse(BaseModel):
    """Schema for assessment status response"""
    can_take_assessment: bool
    last_assessment_date: Optional[str]
    next_available_date: Optional[str]
    message: str
