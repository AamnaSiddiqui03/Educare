from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.data.db import get_db
from app.data.schema import (
    AssessmentStartResponse,
    AssessmentSubmitRequest,
    AssessmentSubmitResponse,
    AssessmentReportResponse,
    StudentAssessmentHistoryResponse,
    AvailableAssessmentResponse,
    AssessmentStatusResponse,
    TokenData
)
from app.services.assessment_service import AssessmentService
from app.services.student_service import StudentService
from app.core.deps import get_current_active_user

router = APIRouter()


@router.get("/{user_id}/assessment/available", response_model=List[AvailableAssessmentResponse])
async def get_available_assessments(
    user_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get list of available assessments for student
    
    Returns all active assessments that the student can take
    """
    # Check if user is trying to access their own assessments
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own assessments"
        )
    
    try:
        # Verify student exists
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        assessments = AssessmentService.get_available_assessments(db)
        
        return [
            AvailableAssessmentResponse(
                assessment_id=str(assessment.assessment_id),
                assessment_name=assessment.assessment_name,
                assessment_type=assessment.assessment_type,
                description=assessment.description,
                total_questions=assessment.total_questions,
                time_limit_minutes=assessment.time_limit_minutes
            )
            for assessment in assessments
        ]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving available assessments"
        )


@router.get("/{user_id}/assessment/start/{assessment_id}", response_model=AssessmentStartResponse)
async def start_assessment(
    user_id: str,
    assessment_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start assessment - Get assessment questions
    
    Returns assessment details and questions for the student to answer
    """
    # Check if user is trying to start their own assessment
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only start your own assessments"
        )
    
    try:
        # Verify student exists
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Get assessment details
        assessment = AssessmentService.get_assessment_by_id(db, assessment_id)
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found or inactive"
            )
        
        # Check if student can take this assessment
        status_check = AssessmentService.can_student_take_assessment(db, str(student.student_id), assessment_id)
        if not status_check["can_take_assessment"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=status_check["message"]
            )
        
        # Get assessment questions (from external source)
        questions = AssessmentService.get_assessment_questions(assessment_id)
        
        return AssessmentStartResponse(
            assessment_id=str(assessment.assessment_id),
            assessment_name=assessment.assessment_name,
            assessment_type=assessment.assessment_type,
            description=assessment.description,
            total_questions=assessment.total_questions,
            time_limit_minutes=assessment.time_limit_minutes,
            questions=questions,
            message="Assessment started successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while starting assessment"
        )


@router.post("/{user_id}/assessment/submit/{assessment_id}", response_model=AssessmentSubmitResponse)
async def submit_assessment(
    user_id: str,
    assessment_id: str,
    submission_data: AssessmentSubmitRequest,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit assessment answers
    
    Submit student's answers and generate PDF report
    """
    # Check if user is trying to submit their own assessment
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit your own assessments"
        )
    
    try:
        # Verify student exists
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Get assessment details for response
        assessment = AssessmentService.get_assessment_by_id(db, assessment_id)
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found or inactive"
            )
        
        # Submit assessment
        submission = AssessmentService.submit_assessment(
            db=db,
            student_id=str(student.student_id),
            assessment_id=assessment_id,
            answers=submission_data.answers
        )
        
        return AssessmentSubmitResponse(
            submission_id=str(submission.submission_id),
            assessment_id=str(submission.assessment_id),
            assessment_name=assessment.assessment_name,
            assessment_completed=student.assessment_completed,
            report_pdf_url=submission.report_pdf_url,
            submitted_at=submission.submitted_at.isoformat(),
            message="Assessment submitted successfully. Profile is now visible to donors."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while submitting assessment"
        )


@router.get("/{user_id}/assessment/report/{submission_id}", response_model=AssessmentReportResponse)
async def get_assessment_report(
    user_id: str,
    submission_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Download PDF assessment report
    
    Returns the PDF report URL for the specified assessment submission
    """
    # Check if user is trying to access their own report
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own assessment reports"
        )
    
    try:
        # Verify student exists
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Get assessment submission
        submission = AssessmentService.get_assessment_report(db, submission_id)
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment submission not found"
            )
        
        # Verify the submission belongs to this student
        if str(submission.student_id) != str(student.student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own assessment reports"
            )
        
        # Get assessment details
        assessment = AssessmentService.get_assessment_by_id(db, str(submission.assessment_id))
        
        return AssessmentReportResponse(
            submission_id=str(submission.submission_id),
            student_id=str(submission.student_id),
            assessment_id=str(submission.assessment_id),
            assessment_name=assessment.assessment_name if assessment else "Unknown Assessment",
            report_pdf_url=submission.report_pdf_url,
            submitted_at=submission.submitted_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving assessment report"
        )


@router.get("/{user_id}/assessment/history", response_model=List[StudentAssessmentHistoryResponse])
async def get_assessment_history(
    user_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get student's assessment history
    
    Returns list of all assessment submissions by the student
    """
    # Check if user is trying to access their own history
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own assessment history"
        )
    
    try:
        # Verify student exists
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Get assessment history
        submissions = AssessmentService.get_student_assessments(db, str(student.student_id))
        
        # Get assessment details for each submission
        history = []
        for submission in submissions:
            assessment = AssessmentService.get_assessment_by_id(db, str(submission.assessment_id))
            history.append(StudentAssessmentHistoryResponse(
                submission_id=str(submission.submission_id),
                assessment_id=str(submission.assessment_id),
                assessment_name=assessment.assessment_name if assessment else "Unknown Assessment",
                assessment_type=assessment.assessment_type if assessment else "Unknown",
                report_pdf_url=submission.report_pdf_url,
                submitted_at=submission.submitted_at.isoformat()
            ))
        
        return history
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving assessment history"
        )
