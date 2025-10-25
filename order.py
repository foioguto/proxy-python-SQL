from model import *

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Text, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"))

    def __repr__(self):
        return f"<Order(id={self.id}, numero='{self.number}')>"
    