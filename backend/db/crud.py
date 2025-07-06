from sqlalchemy.orm import Session
from backend.db.models import ResumeData,HRData,ShortlistData
from backend.db.database import SessionLocal
from typing import List, Dict
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# function for converting sql objects to dictionary
def resume_data_to_dict(candidate: ResumeData) -> Dict:
    """Convert ResumeData ORM object to dictionary"""
    return {
        'id': candidate.id,
        'name':candidate.name,
        'college_name': candidate.college_name,
        'tenth_percent': candidate.tenth_percent,
        'twelfth_percent': candidate.twelfth_percent,
        'cgpa': candidate.cgpa,
        'skills': candidate.skills,
    }

# function for sorting candidates by 10th percentage
def sort_candidates_by_10th(db:Session):
    return db.query(ShortlistData).order_by(ShortlistData.tenth_percent.desc()).all()

# function for sorting candidates by 12th percentage
def sort_candidates_by_12th(db:Session):
    return db.query(ShortlistData).order_by(ShortlistData.twelfth_percent.desc()).all()

# function for sorting candidates by cgpa
def sort_candidates_by_cgpa(db:Session):
   return db.query(ShortlistData).order_by(ShortlistData.cgpa.desc()).all()
    # return [resume_data_to_dict(c) for c in sorted_candidates]

# function for sorting candidates by weighted score
def sort_candidates_by_weighted_score(db: Session):
    """
    Sort candidates in ShortlistData based on the weighted score formula:
    0.4*CGPA + 0.2*10th% + 0.3*12th% + 0.1*cosine_score
    """
    # Calculate the weighted score expression
    weighted_score = (
        0.4 * ShortlistData.cgpa +
        0.2 * ShortlistData.tenth_percent +
        0.3 * ShortlistData.twelfth_percent +
        0.1 * ShortlistData.cosine_score
    )
    
    sorted_candidates = db.query(ShortlistData).order_by(weighted_score.desc()).all()
    return sorted_candidates

# function to filter candidates based on 10th,12th and cgpa
def filter_candidates(db: Session, cgpa_threshold: float, tenth_threshold: float, twelfth_threshold: float):
    return db.query(ResumeData).filter(
        ResumeData.cgpa >= cgpa_threshold,
        ResumeData.tenth_percent >= tenth_threshold,
        ResumeData.twelfth_percent >= twelfth_threshold
    ).all()

# function to add resume data
def add_resume_data(db: Session, data: Dict):
    """
    Inserts a candidate's resume data into the database.

    :param db: Database session
    :param data: Dictionary containing candidate details
    """

    new_candidate = ResumeData(
        name=data.get("name"),
        college_name=data.get("college name"),
        tenth_percent=data.get("10th percent"),
        twelfth_percent=data.get("12th or diploma percentage"),
        cgpa=data.get("CGPA"),
        skills=data.get("skills")  
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)  
    return new_candidate

# Inserts skill data into the hr_db table.
def add_skill_data(db: Session, data: Dict):
    db.query(HRData).delete()
    db.commit()
    skills = data.get("required_skills", [])  
    if not isinstance(skills, list):
        skills = [skills]  
    skills = [str(skill) for skill in skills if skill is not None]
    
    new_skill = HRData(
        skill_name=skills  
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

# Store filtered candidates with cosine scores in shortlist_data table
def add_shortlist_data(db: Session, candidates_with_scores: list):
    try:
        db.query(ShortlistData).delete() #deleting past shortlist data
        
        for candidate, score in candidates_with_scores:  
            new_entry = ShortlistData(
                name=candidate["name"],
                college_name=candidate["college_name"],
                tenth_percent=candidate["tenth_percent"],
                twelfth_percent=candidate["twelfth_percent"],
                cgpa=candidate["cgpa"],
                skills=candidate["skills"], 
                cosine_score=score  
            )
            db.add(new_entry)

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e

#   Retrieve required skills from HRData table
def get_required_skills(db: Session):
    hr_skills = db.query(HRData).all()
    required_skills = []
    
    for entry in hr_skills:
        if entry.skill_name is None:
            continue  
    
        if isinstance(entry.skill_name, str):
            try:
                skills = json.loads(entry.skill_name)
            except json.JSONDecodeError:
                skills = []
        else:
            skills = entry.skill_name
        
        if isinstance(skills, list):
            required_skills.extend([skill for skill in skills if skill is not None])
    
    return required_skills



# Compute cosine similarity between candidates' skills and required skills.
def compute_cosine_similarity(candidates, required_skills):
    # Filter out None values from required_skills
    required_skills = [skill for skill in required_skills if skill is not None]
    
    if not required_skills:
        raise ValueError("No valid required skills provided for cosine similarity calculation.")
    
    # Convert JSON skills to text format (comma-separated)
    candidate_texts = [
        ", ".join(json.loads(c.skills)) if isinstance(c.skills, str) else ", ".join(c.skills) 
        for c in candidates
    ]
    required_skills_text = ", ".join(required_skills)  # Convert required skills to a string

    # Vectorize skills using TF-IDF
    vectorizer = TfidfVectorizer()
    skill_vectors = vectorizer.fit_transform([required_skills_text] + candidate_texts)  # First is required skills, rest are candidates

    # Compute cosine similarity (first row is required skills)
    similarities = cosine_similarity(skill_vectors[0:1], skill_vectors[1:])[0]

    # Attach similarity scores to candidates
    candidate_scores = [(candidates[i], similarities[i]) for i in range(len(candidates))]

    # Sort candidates by similarity (higher is better)
    sorted_candidates = sorted(candidate_scores, key=lambda x: x[1], reverse=True)

    # Convert to dictionary format and return
    return [{"candidate": resume_data_to_dict(c[0]), "cosine_score": c[1]} for c in sorted_candidates]

