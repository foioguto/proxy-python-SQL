class Cliente:
    def __init__(self, id, nome, db_conn):
        self.id = id
        self.nome = nome
        self._db_conn = db_conn
        self._pedidos = []
    

    def fazer_pedido(self):
        while True:
            try:
                user_input = input("Digite o número do pedido\n")
                pedido_atual = int(user_input)
                break  
            except ValueError:
                print("Entrada inválida. Por favor, digite apenas números inteiros.")

        self.listar_pedidos = pedido_atual

        print(f"Pedido {pedido_atual} adicionado.")

        return self._pedidos
    

    @property
    def listar_pedidos(self):
        return self._pedidos
    

    @listar_pedidos.setter
    def listar_pedidos(self, novo_pedido):
        if not isinstance(novo_pedido, int):
            raise TypeError("O pedido deve ser um número inteiro.")
        
        self._pedidos.append(novo_pedido)
    

cliente1 = Cliente(id=1, nome="João", db_conn=None)
print(cliente1.fazer_pedido())
