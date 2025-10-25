from model import *

__tablename__ = "clientes"
    
id = Column(Integer, primary_key=True)
nome = Column(String)

# Lazy Loading por padrão (lazy='select'): Pedidos só são carregados do DB
# quando a propriedade 'pedidos' é acessada.
pedidos = relationship("Pedido", backref="cliente", lazy="select")

def __repr__(self):
# O __repr__ de classes ORM não deve acessar relacionamentos lazy para evitar SELECTs indesejadas
    return f"<ClienteORM(id={self.id}, nome='{self.nome}')>"

# Cria as tabelas no banco (apenas se for a primeira execução)
Base.metadata.create_all(bind=engine)