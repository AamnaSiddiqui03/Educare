from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text           # <--- important!
from app.data import get_db

app = FastAPI()

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Wrap raw SQL in text()
        db.execute(text("SELECT 1"))
        return {"status": "Connected to PostgreSQL!"}
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}
