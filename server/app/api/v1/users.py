from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union, List

from app.data.db import get_db
from app.data.schema import UserDetailResponse, TokenData
from app.services.user_service import UserService
from app.core.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[UserDetailResponse])
async def get_all_users(
    db: Session = Depends(get_db)
):
    """
    Get all users
    
    Returns a list of all users in the system.
    No authentication required.
    """
    users = UserService.get_all_users(db)
    
    return [
        UserDetailResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            role=user.role,
            verified=user.verified,
            created_at=user.created_at.isoformat()
        )
        for user in users
    ]


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user_details(
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user's details
    
    Convenience endpoint to get the current user's own details
    """
    user = UserService.get_user_by_id(db, current_user.user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserDetailResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        role=user.role,
        verified=user.verified,
        created_at=user.created_at.isoformat()
    )


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user_details(
    user_id: str,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user details by user ID
    
    - **user_id**: The UUID of the user to retrieve
    
    Returns user details based on the authenticated user's permissions.
    Users can only view their own details.
    """
    # Check if user is trying to access their own data
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own user details"
        )
    
    # Get user from database
    user = UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserDetailResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        role=user.role,
        verified=user.verified,
        created_at=user.created_at.isoformat()
    )
