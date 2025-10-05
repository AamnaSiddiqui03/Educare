from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List
import uuid

from app.data.models import Student, StudentEducation, StudentAssessment, AssessmentMaster, User, UserRole


class StudentService:
    """Service for student-related operations"""
    
    @staticmethod
    def get_student_by_user_id(db: Session, user_id: str) -> Optional[Student]:
        """Get student by user ID"""
        return db.query(Student).filter(Student.user_id == user_id).first()
    
    @staticmethod
    def get_student_by_id(db: Session, student_id: str) -> Optional[Student]:
        """Get student by student ID"""
        return db.query(Student).filter(Student.student_id == student_id).first()
    
    @staticmethod
    def create_student_profile(
        db: Session, 
        user_id: str, 
        phone: str, 
        address: str, 
        help_text: str,
        photo_url: Optional[str] = None,
        video_url: Optional[str] = None,
        # Personal Information
        gender: Optional[str] = None,
        age: Optional[int] = None,
        # Parent/Guardian Information
        parent_guardian_occupation: Optional[str] = None,
        parent_guardian_monthly_income: Optional[int] = None,
        parents_education_status: Optional[str] = None,
        parent_live_status: Optional[str] = None,
        # Scholarship Information
        scholarship_amount_requested: Optional[int] = None,
        is_eligible_for_zakat: Optional[bool] = None,
        # Applicant Information
        applicant_email: Optional[str] = None,
        applicant_type: Optional[str] = None,
        applicant_name: Optional[str] = None,
        applicant_mobile_number: Optional[str] = None
    ) -> Student:
        """Create a new student profile"""
        # Check if user exists and is a student
        user = db.query(User).filter(User.id == user_id, User.role == UserRole.STUDENT).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or not a student"
            )
        
        # Check if student profile already exists
        existing_student = StudentService.get_student_by_user_id(db, user_id)
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student profile already exists"
            )
        
        # Create student profile
        student = Student(
            user_id=user_id,
            phone=phone,
            address=address,
            help_text=help_text,
            photo_url=photo_url,
            video_url=video_url,
            # Personal Information
            gender=gender.value if gender else None,
            age=age,
            # Parent/Guardian Information
            parent_guardian_occupation=parent_guardian_occupation,
            parent_guardian_monthly_income=parent_guardian_monthly_income,
            parents_education_status=parents_education_status,
            parent_live_status=parent_live_status.value if parent_live_status else None,
            # Scholarship Information
            scholarship_amount_requested=scholarship_amount_requested,
            is_eligible_for_zakat=is_eligible_for_zakat,
            # Applicant Information
            applicant_email=applicant_email,
            applicant_type=applicant_type.value if applicant_type else None,
            applicant_name=applicant_name,
            applicant_mobile_number=applicant_mobile_number
        )
        
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def update_student_profile(
        db: Session, 
        student_id: str, 
        phone: Optional[str] = None,
        address: Optional[str] = None,
        help_text: Optional[str] = None,
        photo_url: Optional[str] = None,
        video_url: Optional[str] = None,
        # Personal Information
        gender: Optional[str] = None,
        age: Optional[int] = None,
        # Parent/Guardian Information
        parent_guardian_occupation: Optional[str] = None,
        parent_guardian_monthly_income: Optional[int] = None,
        parents_education_status: Optional[str] = None,
        parent_live_status: Optional[str] = None,
        # Scholarship Information
        scholarship_amount_requested: Optional[int] = None,
        is_eligible_for_zakat: Optional[bool] = None,
        # Applicant Information
        applicant_email: Optional[str] = None,
        applicant_type: Optional[str] = None,
        applicant_name: Optional[str] = None,
        applicant_mobile_number: Optional[str] = None
    ) -> Student:
        """Update student profile"""
        student = StudentService.get_student_by_id(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Update only provided fields
        if phone is not None:
            student.phone = phone
        if address is not None:
            student.address = address
        if help_text is not None:
            student.help_text = help_text
        if photo_url is not None:
            student.photo_url = photo_url
        if video_url is not None:
            student.video_url = video_url
        
        # Personal Information
        if gender is not None:
            student.gender = gender.value if hasattr(gender, 'value') else gender
        if age is not None:
            student.age = age
        
        # Parent/Guardian Information
        if parent_guardian_occupation is not None:
            student.parent_guardian_occupation = parent_guardian_occupation
        if parent_guardian_monthly_income is not None:
            student.parent_guardian_monthly_income = parent_guardian_monthly_income
        if parents_education_status is not None:
            student.parents_education_status = parents_education_status
        if parent_live_status is not None:
            student.parent_live_status = parent_live_status.value if hasattr(parent_live_status, 'value') else parent_live_status
        
        # Scholarship Information
        if scholarship_amount_requested is not None:
            student.scholarship_amount_requested = scholarship_amount_requested
        if is_eligible_for_zakat is not None:
            student.is_eligible_for_zakat = is_eligible_for_zakat
        
        # Applicant Information
        if applicant_email is not None:
            student.applicant_email = applicant_email
        if applicant_type is not None:
            student.applicant_type = applicant_type.value if hasattr(applicant_type, 'value') else applicant_type
        if applicant_name is not None:
            student.applicant_name = applicant_name
        if applicant_mobile_number is not None:
            student.applicant_mobile_number = applicant_mobile_number
        
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def mark_profile_completed(db: Session, student_id: str) -> Student:
        """Mark student profile as completed"""
        student = StudentService.get_student_by_id(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        student.profile_completed = True
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def get_student_progress(db: Session, student_id: str) -> dict:
        """Get student progress status"""
        student = StudentService.get_student_by_id(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        return {
            "profile_completed": student.profile_completed,
            "assessment_completed": student.assessment_completed,
            "message": "Student progress retrieved successfully"
        }
    
    # Education methods
    @staticmethod
    def get_education_entries(db: Session, student_id: str) -> List[StudentEducation]:
        """Get all education entries for a student"""
        student = StudentService.get_student_by_id(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        return db.query(StudentEducation).filter(
            StudentEducation.student_id == student_id
        ).order_by(StudentEducation.created_at.desc()).all()
    
    @staticmethod
    def add_education_entry(
        db: Session,
        student_id: str,
        institution_name: str,
        education_level: str,
        year_of_passing: str,
        marks_obtained: Optional[str] = None,
        report_card_url: Optional[str] = None
    ) -> StudentEducation:
        """Add new education entry for student"""
        student = StudentService.get_student_by_id(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        education = StudentEducation(
            student_id=student_id,
            institution_name=institution_name,
            education_level=education_level,
            year_of_passing=year_of_passing,
            marks_obtained=marks_obtained,
            report_card_url=report_card_url
        )
        
        db.add(education)
        db.commit()
        db.refresh(education)
        return education
    
    @staticmethod
    def update_education_entry(
        db: Session,
        education_id: str,
        institution_name: Optional[str] = None,
        education_level: Optional[str] = None,
        year_of_passing: Optional[str] = None,
        marks_obtained: Optional[str] = None,
        report_card_url: Optional[str] = None
    ) -> StudentEducation:
        """Update education entry"""
        education = db.query(StudentEducation).filter(
            StudentEducation.education_id == education_id
        ).first()
        
        if not education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education entry not found"
            )
        
        # Update only provided fields
        if institution_name is not None:
            education.institution_name = institution_name
        if education_level is not None:
            education.education_level = education_level
        if year_of_passing is not None:
            education.year_of_passing = year_of_passing
        if marks_obtained is not None:
            education.marks_obtained = marks_obtained
        if report_card_url is not None:
            education.report_card_url = report_card_url
        
        db.commit()
        db.refresh(education)
        return education
    
    @staticmethod
    def delete_education_entry(db: Session, education_id: str) -> bool:
        """Delete education entry"""
        education = db.query(StudentEducation).filter(
            StudentEducation.education_id == education_id
        ).first()
        
        if not education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education entry not found"
            )
        
        db.delete(education)
        db.commit()
        return True
