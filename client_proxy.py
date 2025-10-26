# client_proxy.py - The Virtual Proxy Implementation

from sqlalchemy import select
from clientORM import ClientORM
from order import Order
from model import SessionLocal

class ClientProxy:
    """
    A Virtual Proxy for the ClientORM object.
    It implements Lazy Initialization by deferring the database load 
    until the 'Real Subject' (ClientORM instance) is first needed.
    """
    def __init__(self, client_id):
        """
        Initializes the Proxy with the client's ID.
        NOTE: The real client object is NOT loaded from the DB here.
        """
        self.client_id = client_id
        self._real_client = None  # The Real Subject (ClientORM) starts as None
        self._db = SessionLocal() # A DB session is opened immediately

    def _load_client(self):
        """
        Implements Lazy Initialization. Loads the ClientORM object from the database 
        only if it hasn't been loaded yet.
        """
        if self._real_client is None:
            print(">>> [Proxy] Loading client from database...")
            # Query the database for the client
            stmt = select(ClientORM).filter(ClientORM.id == self.client_id)
            self._real_client = self._db.scalars(stmt).first()
            if not self._real_client:
                # If client is not found, raise an error
                raise ValueError(f"Client with id={self.client_id} not found.")
        return self._real_client

    @property
    def name(self):
        """Public interface property. Triggers _load_client (Lazy Initialization)."""
        real = self._load_client()
        return real.name

    @property
    def orders(self):
        """
        Public interface property. Triggers _load_client and then delegates 
        the call, which triggers SQLAlchemy's Lazy Loading for the orders.
        """
        real = self._load_client()
        print(">>> [Proxy] Lazy loading orders...")
        return real.orders

    def add_order(self, number):
        """
        Public interface method. Creates a new order and commits it to the database.
        Triggers _load_client if the real object hasn't been loaded yet.
        """
        real = self._load_client()
        print(f">>> [Proxy] Creating order {number} for {real.name}...")
        order = Order(number=number, client=real)
        self._db.add(order)
        self._db.commit()
        print(f">>> Order {number} added.")

    # Select operation (Wrapper for getting client details)
    def get_client_info(self):
        """
        Retrieves comprehensive client information, including the order count.
        Accessing len(real.orders) will trigger both Lazy Initialization 
        (if not loaded) and Lazy Loading of orders.
        """
        real = self._load_client()
        print(f">>> [Proxy] Client info: id={real.id}, name={real.name}, orders_count={len(real.orders)}")
        return {
            "id": real.id,
            "name": real.name,
            "orders_count": len(real.orders)
        }

    # Insert operation (Wrapper for creating a single order)
    def create_order(self, number):
        """
        Delegates the creation of a new order to the real client object.
        """
        real = self._load_client()
        print(f">>> [Proxy] Adding order {number} for {real.name}...")
        new_order = Order(number=number, client=real)
        self._db.add(new_order)
        self._db.commit()
        print(f">>> [Proxy] Order {number} inserted successfully.")

    def close(self):
        """Closes the underlying SQLAlchemy database session."""
        print(">>> [Proxy] Closing DB session.")
        self._db.close()