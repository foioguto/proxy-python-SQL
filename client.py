from sqlalchemy.orm import make_transient
from clientORM import ClientORM
from model import *

class Client:
    def __init__(self, id, name, db_conn):
        self.id = id
        self.name = name
        self._db_conn = db_conn
        self._orders = []
        self._orm_instance = None

        with next(get_db()) as db:
            self._orm_instance = db.query(ClientORM).filter(ClientORM.id == id).first()
            if not self._orm_instance:
                self._orm_instance = ClientORM(id=id, name=name)
                db.add(self._orm_instance)
                db.commit()
                db.refresh(self._orm_instance)
    
    def __repr__(self):
        return repr(self._orm_instance)


    def process_order(self):
        while True:
            try:
                user_input = input("Type the order number\n")
                current_order = int(user_input)
                break  
            except ValueError:
                print("Invalid input. Type only integer number")

        self.list_orders = current_order

        print(f"Order {current_order} added.")

        return self._orders
    

    @property
    def list_orders(self):
        return self._orm_instance.orders
    

    @list_orders.setter
    def list_orders(self, new_order):
        if not isinstance(new_order, int):
            raise TypeError("Only integer numbers.")
        
        self._orders.append(new_order)
    

client1 = Client(id=1, name="João", db_conn=None)
print(client1.process_order())
