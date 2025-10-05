from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.schema import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
    StudentProgressResponse
)
from app.services.student_service import StudentService

router = APIRouter()


@router.post("/{user_id}/profile", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_student_profile(
    user_id: str,
    profile_data: StudentProfileCreate,
    db: Session = Depends(get_db)
):
    """
    Create student profile after registration
    
    - **phone**: Student phone number
    - **address**: Student address
    - **photo_url**: Optional profile photo URL
    - **video_url**: Optional video introduction URL
    - **help_text**: Text describing kind of help student is seeking
    """
    
    try:
        student = StudentService.create_student_profile(
            db=db,
            user_id=user_id,
            phone=profile_data.phone,
            address=profile_data.address,
            help_text=profile_data.help_text,
            photo_url=profile_data.photo_url,
            video_url=profile_data.video_url,
            # Personal Information
            gender=profile_data.gender,
            age=profile_data.age,
            # Parent/Guardian Information
            parent_guardian_occupation=profile_data.parent_guardian_occupation,
            parent_guardian_monthly_income=profile_data.parent_guardian_monthly_income,
            parents_education_status=profile_data.parents_education_status,
            parent_live_status=profile_data.parent_live_status,
            # Scholarship Information
            scholarship_amount_requested=profile_data.scholarship_amount_requested,
            is_eligible_for_zakat=profile_data.is_eligible_for_zakat,
            # Applicant Information
            applicant_email=profile_data.applicant_email,
            applicant_type=profile_data.applicant_type,
            applicant_name=profile_data.applicant_name,
            applicant_mobile_number=profile_data.applicant_mobile_number
        )
        
        return StudentProfileResponse(
            student_id=str(student.student_id),
            user_id=str(student.user_id),
            phone=student.phone,
            address=student.address,
            photo_url=student.photo_url,
            video_url=student.video_url,
            help_text=student.help_text,
            # Personal Information
            gender=student.gender,
            age=student.age,
            # Parent/Guardian Information
            parent_guardian_occupation=student.parent_guardian_occupation,
            parent_guardian_monthly_income=student.parent_guardian_monthly_income,
            parents_education_status=student.parents_education_status,
            parent_live_status=student.parent_live_status,
            # Scholarship Information
            scholarship_amount_requested=student.scholarship_amount_requested,
            is_eligible_for_zakat=student.is_eligible_for_zakat,
            # Applicant Information
            applicant_email=student.applicant_email,
            applicant_type=student.applicant_type,
            applicant_name=student.applicant_name,
            applicant_mobile_number=student.applicant_mobile_number,
            # Status Fields
            profile_completed=student.profile_completed,
            assessment_completed=student.assessment_completed,
            created_at=student.created_at.isoformat(),
            updated_at=student.updated_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating student profile"
        )


@router.get("/{user_id}/profile", response_model=StudentProfileResponse)
async def get_student_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get student profile
    
    Returns the student's profile information
    """
    
    student = StudentService.get_student_by_user_id(db, user_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    return StudentProfileResponse(
        student_id=str(student.student_id),
        user_id=str(student.user_id),
        phone=student.phone,
        address=student.address,
        photo_url=student.photo_url,
        video_url=student.video_url,
        help_text=student.help_text,
        # Personal Information
        gender=student.gender,
        age=student.age,
        # Parent/Guardian Information
        parent_guardian_occupation=student.parent_guardian_occupation,
        parent_guardian_monthly_income=student.parent_guardian_monthly_income,
        parents_education_status=student.parents_education_status,
        parent_live_status=student.parent_live_status,
        # Scholarship Information
        scholarship_amount_requested=student.scholarship_amount_requested,
        is_eligible_for_zakat=student.is_eligible_for_zakat,
        # Applicant Information
        applicant_email=student.applicant_email,
        applicant_type=student.applicant_type,
        applicant_name=student.applicant_name,
        applicant_mobile_number=student.applicant_mobile_number,
        # Status Fields
        profile_completed=student.profile_completed,
        assessment_completed=student.assessment_completed,
        created_at=student.created_at.isoformat(),
        updated_at=student.updated_at.isoformat()
    )


@router.put("/{user_id}/profile", response_model=StudentProfileResponse)
async def update_student_profile(
    user_id: str,
    profile_data: StudentProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Update student profile
    
    Updates the student's profile information with provided fields
    """
    
    student = StudentService.get_student_by_user_id(db, user_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    try:
        updated_student = StudentService.update_student_profile(
            db=db,
            student_id=str(student.student_id),
            phone=profile_data.phone,
            address=profile_data.address,
            help_text=profile_data.help_text,
            photo_url=profile_data.photo_url,
            video_url=profile_data.video_url,
            # Personal Information
            gender=profile_data.gender,
            age=profile_data.age,
            # Parent/Guardian Information
            parent_guardian_occupation=profile_data.parent_guardian_occupation,
            parent_guardian_monthly_income=profile_data.parent_guardian_monthly_income,
            parents_education_status=profile_data.parents_education_status,
            parent_live_status=profile_data.parent_live_status,
            # Scholarship Information
            scholarship_amount_requested=profile_data.scholarship_amount_requested,
            is_eligible_for_zakat=profile_data.is_eligible_for_zakat,
            # Applicant Information
            applicant_email=profile_data.applicant_email,
            applicant_type=profile_data.applicant_type,
            applicant_name=profile_data.applicant_name,
            applicant_mobile_number=profile_data.applicant_mobile_number
        )
        
        return StudentProfileResponse(
            student_id=str(updated_student.student_id),
            user_id=str(updated_student.user_id),
            phone=updated_student.phone,
            address=updated_student.address,
            photo_url=updated_student.photo_url,
            video_url=updated_student.video_url,
            help_text=updated_student.help_text,
            # Personal Information
            gender=updated_student.gender,
            age=updated_student.age,
            # Parent/Guardian Information
            parent_guardian_occupation=updated_student.parent_guardian_occupation,
            parent_guardian_monthly_income=updated_student.parent_guardian_monthly_income,
            parents_education_status=updated_student.parents_education_status,
            parent_live_status=updated_student.parent_live_status,
            # Scholarship Information
            scholarship_amount_requested=updated_student.scholarship_amount_requested,
            is_eligible_for_zakat=updated_student.is_eligible_for_zakat,
            # Applicant Information
            applicant_email=updated_student.applicant_email,
            applicant_type=updated_student.applicant_type,
            applicant_name=updated_student.applicant_name,
            applicant_mobile_number=updated_student.applicant_mobile_number,
            # Status Fields
            profile_completed=updated_student.profile_completed,
            assessment_completed=updated_student.assessment_completed,
            created_at=updated_student.created_at.isoformat(),
            updated_at=updated_student.updated_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating student profile"
        )


@router.post("/{user_id}/profile/submit", response_model=StudentProgressResponse)
async def submit_student_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Mark profile as completed (profile_completed = true)
    
    Triggers Phase 2 in portal
    """
    
    student = StudentService.get_student_by_user_id(db, user_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    try:
        StudentService.mark_profile_completed(db, str(student.student_id))
        
        return StudentProgressResponse(
            profile_completed=True,
            assessment_completed=student.assessment_completed,
            message="Profile completed successfully. You can now proceed to assessments."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while submitting student profile"
        )


@router.get("/{user_id}/profile/progress", response_model=StudentProgressResponse)
async def get_student_progress(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get student progress status
    
    Returns profile_completed + assessment_completed for frontend tracker
    """
    
    student = StudentService.get_student_by_user_id(db, user_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    try:
        progress = StudentService.get_student_progress(db, str(student.student_id))
        return StudentProgressResponse(**progress)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving student progress"
        )
