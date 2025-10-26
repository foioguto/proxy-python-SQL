# clientORM.py - SQLAlchemy ORM Model for Clients (The Real Subject)

from model import *

class ClientORM(Base):
    """
    SQLAlchemy model for the 'clients' table.
    This is the 'Real Subject' that the Proxy will control access to.
    """
    __tablename__ = "clients"
        
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationship to the Order model.
    # The default 'lazy='select'' ensures Lazy Loading: Orders are only loaded from the DB 
    # when the 'orders' property is explicitly accessed.
    orders = relationship("Order", backref="client", lazy="select")

    def __repr__(self):
        """
        String representation of the ClientORM object.
        NOTE: ORM __repr__ should avoid accessing lazy relationships to prevent 
        unnecessary SELECT statements (N+1 problem).
        """
        return f"<ClientORM(id={self.id}, name='{self.name}')>"