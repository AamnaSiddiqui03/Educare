from pydantic import BaseModel
from typing import Optional
from app.data.models import UserRole


class UserResponse(BaseModel):
    """User response schema (public data)"""
    id: str
    name: str
    email: str
    role: UserRole
    verified: bool
    created_at: str
    
    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    """Detailed user response schema (for authenticated users)"""
    id: str
    name: str
    email: str
    role: UserRole
    verified: bool
    created_at: str
    
    class Config:
        from_attributes = True


class UserRegistrationResponse(BaseModel):
    """User registration response schema"""
    success: bool = True
    message: str = "User registered successfully"
    user: UserResponse


class TokenData(BaseModel):
    """Token payload schema for internal use"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


class BaseResponse(BaseModel):
    """Base response schema with common fields"""
    success: bool = True
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None


class ValidationErrorResponse(ErrorResponse):
    """Validation error response schema"""
    field_errors: Optional[dict] = None


class HealthCheckResponse(BaseModel):
    """Health check response schema"""
    status: str = "healthy"
    timestamp: str
    version: str = "1.0.0"
