from model import *

class ClientORM(Base):
    __tablename__ = "clients"
        
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Lazy Loading por padrão (lazy='select'): Pedidos só são carregados do DB
    # quando a propriedade 'pedidos' é acessada.
    orders = relationship("Order", backref="client", lazy="select")

    def __repr__(self):
    # O __repr__ de classes ORM não deve acessar relacionamentos lazy para evitar SELECTs indesejadas
        return f"<ClientORM(id={self.id}, name='{self.name}')>"
