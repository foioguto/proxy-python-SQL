# model.py - Database Connection and Session Setup

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Database connection URL (PostgreSQL using psycopg2)
# NOTE: Update the credentials (postgres:supra) and database name (futino) as needed.
DB_URL = "postgresql+psycopg2://postgres:supra@localhost:5432/futino" 

# Create the database engine. 'echo=True' enables SQL logging to the console.
engine = create_engine(DB_URL, echo=True)

# Base class for declarative class definitions (required for ORM models)
Base = declarative_base()

# Configure the local session class.
# autocommit=False ensures transactions are managed explicitly.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function to get a database session (common pattern in FastAPI/Flask).
    The session is closed automatically using a try/finally block.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()