from pydantic import BaseModel, EmailStr, validator
from app.data.models import UserRole


# Request Schemas
class UserRegisterRequest(BaseModel):
    """User registration request schema"""
    name: str
    email: EmailStr
    password: str
    role: UserRole
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if len(v.strip()) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v.strip()
    
    @validator('email')
    def validate_email(cls, v):
        if len(v) > 254:  # RFC 5321 limit
            raise ValueError('Email address is too long')
        return v.lower()


class UserLoginRequest(BaseModel):
    """User login request schema"""
    email: EmailStr
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        return v.lower()


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr
    
    @validator('email')
    def validate_email(cls, v):
        return v.lower()


class PasswordChangeRequest(BaseModel):
    """Password change request schema"""
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Response Schemas
class TokenResponse(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LoginResponse(BaseModel):
    """Login response schema"""
    success: bool = True
    message: str = "Login successful"
    token: TokenResponse
    user: dict  # Will be populated with UserResponse data


class LogoutResponse(BaseModel):
    """Logout response schema"""
    success: bool = True
    message: str = "Successfully logged out"
