from client_proxy import ClientProxy

if __name__ == "__main__":
    print("--- Proxy pattern demo ---")

    client = ClientProxy(client_id=1)

    print("\nAccessing name (real object will be loaded now):")
    print(client.name)

    print("\nAccessing orders (lazy loading triggered):")
    print(client.orders)

    print("\nAdding new order:")
    client.add_order(111)

    print("\nAccessing orders again (should include the new one):")
    print(client.orders)

    client.close()
