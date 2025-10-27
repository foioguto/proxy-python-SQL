# app/cleanup_db.py - Script to drop all tables
import os
from dotenv import load_dotenv

# ADD THESE LINES to load .env before importing 'engine'
# This assumes your .env file is inside the 'app' folder
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

from app.src.core import Base, engine

print(">>> Dropping all existing tables...")
# Drops all tables defined in Base.metadata (clients and orders)
Base.metadata.drop_all(bind=engine)
print(">>> Cleanup successful.")