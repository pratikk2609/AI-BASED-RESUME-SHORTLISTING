from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from backend.utils import resume_extract
from backend.db import crud
from backend.db.database import get_db

# Creating router instance
router = APIRouter()

# Route for extracting resume contents
@router.post("/extract-resume-entities")
async def extract_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    resume = resume_extract.generate_response(file)  
    crud.add_resume_data(db, resume)  
    return {"message": resume}