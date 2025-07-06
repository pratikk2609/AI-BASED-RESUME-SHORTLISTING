from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from backend.db import crud
from backend.db.database import get_db

router=APIRouter()


# route for filtering candidates
@router.post("/filter_candidates")
async def filtering_candidates(
    cgpa: float,
    tenth_percent: float,
    twelfth_percent: float,
    db: Session = Depends(get_db)
):
    candidates = crud.filter_candidates(db, cgpa, tenth_percent, twelfth_percent)
    
    required_skills = crud.get_required_skills(db)
    
    if not required_skills:
        return {"message": "No required skills found in HR data. Please add skills first."}
    
    scored_candidates = crud.compute_cosine_similarity(candidates, required_skills)
    
    candidates_with_scores = [
    (c["candidate"], c["cosine_score"])  
    for c in scored_candidates
]

    crud.add_shortlist_data(db, candidates_with_scores)
    
    return [crud.resume_data_to_dict(c) for c in candidates]

# route for sorting shortlisted candidates based on tenth percentage
@router.get("/sort_based_on_tenth")
async def sort_tenth(db:Session=Depends(get_db)):
    candidates=crud.sort_candidates_by_10th(db)
    return [crud.resume_data_to_dict(c) for c in candidates]

# route for sorting candidates based on twelfth percentage
@router.get("/sort_based_on_twelfth")
async def sort_twelfth(db:Session=Depends(get_db)):
    candidates=crud.sort_candidates_by_12th(db)
    return [crud.resume_data_to_dict(c) for c in candidates]

# route for sorting candidates based on cgpa
@router.get("/sort_based_on_cgpa")
async def sort_cgpa(db:Session=Depends(get_db)):
    candidates=crud.sort_candidates_by_cgpa(db)
    return [crud.resume_data_to_dict(c) for c in candidates]

# route for sorting candidates based on weighted sum of 10th,12th,cgpa and cosine score
@router.get("/sort_based_on_weighted_sum")
async def sort_hybrid(db:Session=Depends(get_db)):
    candidates=crud.sort_candidates_by_weighted_score(db)
    return [crud.resume_data_to_dict(c) for c in candidates]