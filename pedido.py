from model import *

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Text, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    def __repr__(self):
        return f"<Pedido(id={self.id}, numero='{self.numero}')>"
    