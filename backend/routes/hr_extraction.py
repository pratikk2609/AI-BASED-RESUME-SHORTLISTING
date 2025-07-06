from fastapi import UploadFile, File,APIRouter
from backend.utils import hr_extract
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from backend.db import crud
from backend.db.database import get_db

#creating router instance
router=APIRouter()


# route for extracting hr skills 
@router.post("/extract-hr-skills")
async def extract_skills(file: UploadFile = File(...), db: Session = Depends(get_db)):
    skills = hr_extract.extract_hr_skills(file)  
    crud.add_skill_data(db, skills) 
    return {"message": skills}