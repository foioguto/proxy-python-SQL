import os
from dotenv import load_dotenv

# ADD THESE LINES to load .env before importing 'engine'
# This assumes your .env file is inside the 'app' folder
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# init_db.py - Database Schema Initialization Script

from app.src.core.model import Base, engine
from app.src.core.clientORM import ClientORM # Import ClientORM to register its metadata
from app.src.core.order import Order      # Import Order to register its metadata

# This script creates all tables defined in Base's metadata (ClientORM and Order)
# in the configured PostgreSQL database.

print("Creating all tables in PostgreSQL database 'futino'...")
Base.metadata.create_all(bind=engine)
print("Done.")