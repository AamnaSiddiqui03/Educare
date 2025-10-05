from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List

from app.data.models import User
from app.services.auth_service import AuthService


class UserService:
    """User service for user management operations"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        """Get all users"""
        return db.query(User).all()
    
    @staticmethod
    def create_user(db: Session, name: str, email: str, password: str, role: str) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        password_hash = AuthService.get_password_hash(password)
        
        # Create user
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
