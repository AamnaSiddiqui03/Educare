from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.data.db import get_db
from app.api.v1 import api_router

app = FastAPI(
    title="NGO Platform API",
    description="API for NGO Platform - Phase 1: Authentication & User Management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "NGO Platform API - Phase 1", "version": "1.0.0"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    """Test database connection"""
    try:
        # Wrap raw SQL in text()
        db.execute(text("SELECT 1"))
        return {"status": "Connected to PostgreSQL!"}
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}
