from sqlalchemy import select
from clientORM import ClientORM
from order import Order
from model import get_db


class Client:
    def __init__(self, id, name, db_conn=None):
        self.id = id
        self.name = name
        self._orders = []
        self._db = next(get_db())  # single session for this client
        self._orm_instance = None

        stmt = select(ClientORM).filter(ClientORM.id == id)
        self._orm_instance = self._db.scalars(stmt).first()

        if not self._orm_instance:
            self._orm_instance = ClientORM(id=id, name=name)
            self._db.add(self._orm_instance)
            self._db.commit()
            self._db.refresh(self._orm_instance)

    def close(self):
        if self._db:
            self._db.close()

    def __repr__(self):
        return repr(self._orm_instance)

    def process_order(self):
        while True:
            try:
                user_input = input("Type the order number\n")
                current_order = int(user_input)
                break
            except ValueError:
                print("Invalid input. Type only integer numbers.")

        # Add to local list
        self.list_orders = current_order

        # Create new order linked to this client
        new_order = Order(number=user_input, client=self._orm_instance)
        self._db.add(new_order)
        self._db.commit()
        self._db.refresh(new_order)

        # Expire 'orders' so SQLAlchemy re-fetches them when accessed next
        self._db.expire(self._orm_instance, ['orders'])

        print(f"Order {current_order} added.")
        return self._orm_instance.orders

    @property
    def list_orders(self):
        return self._orm_instance.orders

    @list_orders.setter
    def list_orders(self, new_order):
        if not isinstance(new_order, int):
            raise TypeError("Only integer numbers are allowed.")
        self._orders.append(new_order)


if __name__ == '__main__':
    print("--- Initializing Client John (ID 1) ---")
    client1 = Client(id=1, name="John")
    print(f"Client Object: {client1}")

    print("\n--- Accessing orders (Lazy Load Triggered) ---")
    initial_orders = client1.list_orders
    print(f"Orders loaded: {initial_orders}")

    print("\n--- Placing a new order ---")
    final_orders = client1.process_order()
    print(f"Final list of orders (after new one): {final_orders}")

    client1.close()
