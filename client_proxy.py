from sqlalchemy import select
from clientORM import ClientORM
from order import Order
from model import SessionLocal

class ClientProxy:
    def __init__(self, client_id):
        self.client_id = client_id
        self._real_client = None
        self._db = SessionLocal()

    def _load_client(self):
        if self._real_client is None:
            print(">>> [Proxy] Loading client from database...")
            stmt = select(ClientORM).filter(ClientORM.id == self.client_id)
            self._real_client = self._db.scalars(stmt).first()
            if not self._real_client:
                raise ValueError(f"Client with id={self.client_id} not found.")
        return self._real_client

    @property
    def name(self):
        real = self._load_client()
        return real.name

    @property
    def orders(self):
        real = self._load_client()
        print(">>> [Proxy] Lazy loading orders...")
        return real.orders

    def add_order(self, number):
        real = self._load_client()
        print(f">>> [Proxy] Creating order {number} for {real.name}...")
        order = Order(number=number, client=real)
        self._db.add(order)
        self._db.commit()
        print(f">>> Order {number} added.")

    #Select
    def get_client_info(self):
        real = self._load_client()
        print(f">>> [Proxy] Client info: id={real.id}, name={real.name}, orders_count={len(real.orders)}")
        return {
            "id": real.id,
            "name": real.name,
            "orders_count": len(real.orders)
        }

    #Insert
    def create_order(self, number):
        real = self._load_client()
        print(f">>> [Proxy] Adding order {number} for {real.name}...")
        new_order = Order(number=number, client=real)
        self._db.add(new_order)
        self._db.commit()
        print(f">>> [Proxy] Order {number} inserted successfully.")

    def close(self):
        self._db.close()
