from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.schema import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
    StudentProgressResponse,
    TokenData
)
from app.services.student_service import StudentService
from app.core.deps import get_current_active_user

router = APIRouter()


@router.post("/{user_id}/profile", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_student_profile(
    user_id: str,
    profile_data: StudentProfileCreate,
    current_user: TokenData = Depends(get_current_active_user),
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
    # Check if user is trying to create their own profile
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create your own student profile"
        )
    
    try:
        student = StudentService.create_student_profile(
            db=db,
            user_id=user_id,
            phone=profile_data.phone,
            address=profile_data.address,
            help_text=profile_data.help_text,
            photo_url=profile_data.photo_url,
            video_url=profile_data.video_url
        )
        
        return StudentProfileResponse(
            student_id=str(student.student_id),
            user_id=str(student.user_id),
            phone=student.phone,
            address=student.address,
            photo_url=student.photo_url,
            video_url=student.video_url,
            help_text=student.help_text,
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
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get student profile
    
    Returns the student's profile information
    """
    # Check if user is trying to access their own profile
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own student profile"
        )
    
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
        profile_completed=student.profile_completed,
        assessment_completed=student.assessment_completed,
        created_at=student.created_at.isoformat(),
        updated_at=student.updated_at.isoformat()
    )


@router.put("/{user_id}/profile", response_model=StudentProfileResponse)
async def update_student_profile(
    user_id: str,
    profile_data: StudentProfileUpdate,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update student profile
    
    Updates the student's profile information with provided fields
    """
    # Check if user is trying to update their own profile
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own student profile"
        )
    
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
            video_url=profile_data.video_url
        )
        
        return StudentProfileResponse(
            student_id=str(updated_student.student_id),
            user_id=str(updated_student.user_id),
            phone=updated_student.phone,
            address=updated_student.address,
            photo_url=updated_student.photo_url,
            video_url=updated_student.video_url,
            help_text=updated_student.help_text,
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
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Mark profile as completed (profile_completed = true)
    
    Triggers Phase 2 in portal
    """
    # Check if user is trying to submit their own profile
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit your own student profile"
        )
    
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
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get student progress status
    
    Returns profile_completed + assessment_completed for frontend tracker
    """
    # Check if user is trying to access their own progress
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own progress"
        )
    
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
