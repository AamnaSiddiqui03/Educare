from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.data.db import get_db
from app.data.schema import (
    EducationCreate,
    EducationUpdate,
    EducationResponse,
    TokenData
)
from app.services.student_service import StudentService
from app.core.deps import get_current_active_user

router = APIRouter()


@router.get("/{user_id}/education", response_model=List[EducationResponse])
async def get_student_education(
    user_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all education entries for a student
    
    Returns list of all education entries for the student
    """
    # Check if user is trying to access their own education
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own education entries"
        )
    
    try:
        # Get student to verify they exist
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        education_entries = StudentService.get_education_entries(db, str(student.student_id))
        
        return [
            EducationResponse(
                education_id=str(entry.education_id),
                student_id=str(entry.student_id),
                institution_name=entry.institution_name,
                education_level=entry.education_level,
                year_of_passing=entry.year_of_passing,
                marks_obtained=entry.marks_obtained,
                report_card_url=entry.report_card_url,
                created_at=entry.created_at.isoformat(),
                updated_at=entry.updated_at.isoformat()
            )
            for entry in education_entries
        ]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving education entries"
        )


@router.post("/{user_id}/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_student_education(
    user_id: str,
    education_data: EducationCreate,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Add new education entry for student
    
    - **institution_name**: School/University name
    - **education_level**: Class 10, Class 12, Undergraduate, etc.
    - **year_of_passing**: Year completed
    - **marks_obtained**: Optional marks/percentage
    - **report_card_url**: Optional upload link
    """
    # Check if user is trying to add to their own education
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add education entries to your own profile"
        )
    
    try:
        # Get student to verify they exist
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        education = StudentService.add_education_entry(
            db=db,
            student_id=str(student.student_id),
            institution_name=education_data.institution_name,
            education_level=education_data.education_level,
            year_of_passing=education_data.year_of_passing,
            marks_obtained=education_data.marks_obtained,
            report_card_url=education_data.report_card_url
        )
        
        return EducationResponse(
            education_id=str(education.education_id),
            student_id=str(education.student_id),
            institution_name=education.institution_name,
            education_level=education.education_level,
            year_of_passing=education.year_of_passing,
            marks_obtained=education.marks_obtained,
            report_card_url=education.report_card_url,
            created_at=education.created_at.isoformat(),
            updated_at=education.updated_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding education entry"
        )


@router.get("/{user_id}/education/{education_id}", response_model=EducationResponse)
async def get_specific_education(
    user_id: str,
    education_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get specific education entry
    
    Returns details of a specific education entry
    """
    # Check if user is trying to access their own education
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own education entries"
        )
    
    try:
        # Get student to verify they exist
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        # Get education entries and find the specific one
        education_entries = StudentService.get_education_entries(db, str(student.student_id))
        education = next((entry for entry in education_entries if str(entry.education_id) == education_id), None)
        
        if not education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education entry not found"
            )
        
        return EducationResponse(
            education_id=str(education.education_id),
            student_id=str(education.student_id),
            institution_name=education.institution_name,
            education_level=education.education_level,
            year_of_passing=education.year_of_passing,
            marks_obtained=education.marks_obtained,
            report_card_url=education.report_card_url,
            created_at=education.created_at.isoformat(),
            updated_at=education.updated_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving education entry"
        )


@router.put("/{user_id}/education/{education_id}", response_model=EducationResponse)
async def update_student_education(
    user_id: str,
    education_id: str,
    education_data: EducationUpdate,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update specific education entry
    
    Updates the specified education entry with provided fields
    """
    # Check if user is trying to update their own education
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own education entries"
        )
    
    try:
        # Get student to verify they exist
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        updated_education = StudentService.update_education_entry(
            db=db,
            education_id=education_id,
            institution_name=education_data.institution_name,
            education_level=education_data.education_level,
            year_of_passing=education_data.year_of_passing,
            marks_obtained=education_data.marks_obtained,
            report_card_url=education_data.report_card_url
        )
        
        return EducationResponse(
            education_id=str(updated_education.education_id),
            student_id=str(updated_education.student_id),
            institution_name=updated_education.institution_name,
            education_level=updated_education.education_level,
            year_of_passing=updated_education.year_of_passing,
            marks_obtained=updated_education.marks_obtained,
            report_card_url=updated_education.report_card_url,
            created_at=updated_education.created_at.isoformat(),
            updated_at=updated_education.updated_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating education entry"
        )


@router.delete("/{user_id}/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_education(
    user_id: str,
    education_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete specific education entry
    
    Removes the specified education entry from the student's profile
    """
    # Check if user is trying to delete their own education
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own education entries"
        )
    
    try:
        # Get student to verify they exist
        student = StudentService.get_student_by_user_id(db, user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found"
            )
        
        StudentService.delete_education_entry(db, education_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting education entry"
        )
