# client.py - Demonstration of the Proxy Pattern usage

from src.gui.client_gui import ClientApp
from src.core.client_proxy import ClientProxy

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()
    print("--- Proxy pattern demo ---")

    # The Proxy object is created, but the Real Subject (ClientORM) is NOT loaded yet.
    client = ClientProxy(client_id=1)

    # 1. Accessing 'name' property
    # This is the first access, triggering Lazy Initialization via _load_client()
    print("\nAccessing name (real object will be loaded now - Lazy Initialization):")
    print(client.name)

    # 2. Accessing 'orders' property
    # The ClientORM is already loaded, but accessing 'orders' triggers 
    # SQLAlchemy's Lazy Loading for the relationship.
    print("\nAccessing orders (lazy loading triggered by SQLAlchemy):")
    print(client.orders)

    # 3. Performing a modifying action
    print("\nAdding new order:")
    # add_order delegates the operation to the already loaded real object.
    client.add_order(111)

    # 4. Verifying the result
    print("\nAccessing orders again (should include the new one):")
    print(client.orders)

    # 5. Closing the DB session
    client.close()