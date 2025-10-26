# order.py - SQLAlchemy ORM Model for Orders

from .model import *

class Order(Base):
    """
    SQLAlchemy model for the 'orders' table.
    """
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Text, nullable=False)
    # Foreign Key linking this order to a client
    client_id = Column(Integer, ForeignKey("clients.id"))

    def __repr__(self):
        """String representation of the Order object."""
        return f"<Order(id={self.id}, number='{self.number}')>"