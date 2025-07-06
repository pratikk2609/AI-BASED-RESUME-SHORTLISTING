from sqlalchemy import Column, Integer, String, JSON, Float
from backend.db.database import Base


# class for resume_data table
class ResumeData(Base):
    __tablename__ = "resume_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(255),nullable=True)
    college_name = Column(String(255), nullable=True)
    tenth_percent = Column(Float, nullable=True)  
    twelfth_percent = Column(Float, nullable=True)  
    cgpa = Column(Float, nullable=True)  
    skills = Column(JSON,nullable=True)  

# class for hr_db table
class HRData(Base):
    __tablename__ = "hr_db"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(JSON)  

# class for shortlist_data table
class ShortlistData(Base):
    __tablename__="shortlist_data"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(255),nullable=True)
    college_name=Column(String(255),nullable=True)
    tenth_percent=Column(Float,nullable=True)
    twelfth_percent=Column(Float,nullable=True)
    cgpa=Column(Float,nullable=True)
    skills=Column(JSON,nullable=True)
    cosine_score=Column(Float,nullable=True)
    
