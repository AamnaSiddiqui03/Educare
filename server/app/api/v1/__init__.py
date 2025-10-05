from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .students import router as students_router
from .student_education import router as education_router
from .student_assessment import router as assessment_router

api_router = APIRouter()

# Include auth routes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include user routes  
api_router.include_router(users_router, prefix="/users", tags=["Users"])

# Include student routes
api_router.include_router(students_router, prefix="/students", tags=["Students"])

# Include education routes
api_router.include_router(education_router, prefix="/students", tags=["Student Education"])

# Include assessment routes
api_router.include_router(assessment_router, prefix="/students", tags=["Student Assessment"])