# init_db.py - Database Schema Initialization Script

from model import Base, engine
from clientORM import ClientORM # Import ClientORM to register its metadata
from order import Order      # Import Order to register its metadata

# This script creates all tables defined in Base's metadata (ClientORM and Order)
# in the configured PostgreSQL database.

print("Creating all tables in PostgreSQL database 'futino'...")
Base.metadata.create_all(bind=engine)
print("Done.")