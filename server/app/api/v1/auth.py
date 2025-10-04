from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.data.db import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.data.schema import (
    UserRegisterRequest,
    UserLoginRequest,
    UserRegistrationResponse,
    LoginResponse,
    LogoutResponse,
    UserResponse,
    TokenResponse
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **name**: User's full name
    - **email**: User's email address (must be unique)
    - **password**: User's password (minimum 8 characters)
    - **role**: User's role (student, donor, or mentor)
    """
    try:
        user = UserService.create_user(
            db=db,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role.value
        )
        
        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            role=user.role,
            verified=user.verified,
            created_at=user.created_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user and return JWT token
    
    - **email**: User's email address
    - **password**: User's password
    """
    # Get user by email
    user = UserService.get_user_by_email(db, login_data.email)
    
    # Check if user exists and password is correct
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not AuthService.verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value
        },
        expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer", expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60)


@router.post("/logout")
async def logout_user():
    """
    Logout user (invalidate session)
    
    Note: With JWT tokens, logout is typically handled client-side by removing the token.
    For server-side invalidation, you would need to implement a token blacklist.
    """
    return LogoutResponse()
