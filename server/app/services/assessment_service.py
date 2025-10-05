from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid

from app.data.models import Student, StudentAssessment, AssessmentMaster


class AssessmentService:
    """Service for assessment-related operations"""
    
    @staticmethod
    def get_available_assessments(db: Session) -> List[AssessmentMaster]:
        """Get all active assessments"""
        return db.query(AssessmentMaster).filter(
            AssessmentMaster.is_active == True
        ).order_by(AssessmentMaster.created_at.desc()).all()
    
    @staticmethod
    def get_assessment_by_id(db: Session, assessment_id: str) -> Optional[AssessmentMaster]:
        """Get assessment by ID"""
        return db.query(AssessmentMaster).filter(
            AssessmentMaster.assessment_id == assessment_id,
            AssessmentMaster.is_active == True
        ).first()
    
    @staticmethod
    def get_assessment_questions(assessment_id: str) -> Dict[str, Any]:
        """
        Get assessment questions from external source
        
        This is a placeholder for external question retrieval.
        In a real implementation, this would fetch from an external API or service.
        """
        # Placeholder questions - replace with actual external API call
        placeholder_questions = {
            "q1": {
                "question": "What is your primary area of interest?",
                "options": ["Technology", "Business", "Arts", "Science"],
                "type": "multiple_choice"
            },
            "q2": {
                "question": "How would you describe your learning style?",
                "options": ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"],
                "type": "multiple_choice"
            },
            "q3": {
                "question": "What motivates you most in your studies?",
                "options": ["Personal Growth", "Career Advancement", "Social Impact", "Financial Security"],
                "type": "multiple_choice"
            }
        }
        
        return placeholder_questions
    
    @staticmethod
    def can_student_take_assessment(db: Session, student_id: str, assessment_id: str) -> Dict[str, Any]:
        """
        Check if student can take assessment (considering refresh intervals)
        
        For now, allowing unlimited attempts. In future, implement refresh intervals.
        """
        # Get last assessment submission for this student and assessment
        last_submission = db.query(StudentAssessment).filter(
            StudentAssessment.student_id == student_id,
            StudentAssessment.assessment_id == assessment_id
        ).order_by(StudentAssessment.submitted_at.desc()).first()
        
        if not last_submission:
            return {
                "can_take_assessment": True,
                "last_assessment_date": None,
                "next_available_date": None,
                "message": "No previous submissions found. You can take this assessment."
            }
        
        # For now, allowing immediate retakes
        # In future, implement refresh intervals (e.g., 30 days)
        return {
            "can_take_assessment": True,
            "last_assessment_date": last_submission.submitted_at.isoformat(),
            "next_available_date": None,
            "message": "You can retake this assessment."
        }
    
    @staticmethod
    def submit_assessment(
        db: Session,
        student_id: str,
        assessment_id: str,
        answers: Dict[str, Any]
    ) -> StudentAssessment:
        """Submit assessment answers and generate PDF report"""
        
        # Verify assessment exists
        assessment = AssessmentService.get_assessment_by_id(db, assessment_id)
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found or inactive"
            )
        
        # Verify student exists
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Generate PDF report URL (placeholder)
        # In a real implementation, this would generate actual PDF
        report_pdf_url = f"https://storage.example.com/assessment_reports/{uuid.uuid4()}.pdf"
        
        # Create assessment submission
        submission = StudentAssessment(
            student_id=student_id,
            assessment_id=assessment_id,
            report_pdf_url=report_pdf_url
        )
        
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        # Update student's assessment completion status
        student.assessment_completed = True
        db.commit()
        
        return submission
    
    @staticmethod
    def get_student_assessments(db: Session, student_id: str) -> List[StudentAssessment]:
        """Get all assessment submissions for a student"""
        return db.query(StudentAssessment).filter(
            StudentAssessment.student_id == student_id
        ).order_by(StudentAssessment.submitted_at.desc()).all()
    
    @staticmethod
    def get_assessment_report(db: Session, submission_id: str) -> Optional[StudentAssessment]:
        """Get specific assessment submission report"""
        return db.query(StudentAssessment).filter(
            StudentAssessment.submission_id == submission_id
        ).first()
    
    @staticmethod
    def delete_assessment_submission(db: Session, submission_id: str) -> bool:
        """Delete assessment submission (admin use)"""
        submission = db.query(StudentAssessment).filter(
            StudentAssessment.submission_id == submission_id
        ).first()
        
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment submission not found"
            )
        
        db.delete(submission)
        db.commit()
        return True
