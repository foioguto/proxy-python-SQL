# app/cleanup_db.py - Script to drop all tables

from app.src.core import Base, engine

print(">>> Dropping all existing tables...")
# Drops all tables defined in Base.metadata (clients and orders)
Base.metadata.drop_all(bind=engine)
print(">>> Cleanup successful.")