from model import Base, engine
from clientORM import ClientORM
from order import Order  # se você tiver um modelo Order definido

print("Creating all tables in PostgreSQL database 'futino'...")
Base.metadata.create_all(bind=engine)
print("Done.")
