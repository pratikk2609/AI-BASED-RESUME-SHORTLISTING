from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read database credentials from environment variables
DATABASE_USER = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_HOST = os.getenv("DB_HOST", "localhost")  # Default to localhost if not set
DATABASE_NAME = os.getenv("DB_NAME")

# Construct database URL
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session and base class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency function for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
