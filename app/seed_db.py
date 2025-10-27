import os
from dotenv import load_dotenv

# ADD THESE LINES to load .env before importing 'engine'
# This assumes your .env file is inside the 'app' folder
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# app/seed_db.py - Script to seed the database

# Uses absolute imports from the 'app' package
from app.src.core import SessionLocal, ClientORM, Order
import random

NUM_CLIENTS = 1000000

# List of 200 words (mix of common names and surnames for simulation)
WORD_LIST = [
    "Alexandre", "Beatriz", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana",
    "Kleber", "Laura", "Marcelo", "Natália", "Otávio", "Patrícia", "Quiteria", "Ricardo", "Sofia", "Thiago",
    "Ursula", "Vinicius", "Wagner", "Xavier", "Yara", "Zeca", "Alice", "Bruno", "Cíntia", "Diego",
    "Elaine", "Fábio", "Gisele", "Hugo", "Ingrid", "Jonas", "Karen", "Luiz", "Mônica", "Nelson",
    "Olivia", "Pedro", "Queiroz", "Raquel", "Sérgio", "Tatiane", "Ulisses", "Valéria", "Wellington", "Yasmin",
    "Zélia", "Ana", "Bento", "Camila", "Davi", "Ester", "Felipe", "Giovanna", "Heitor", "Isabela",
    "João", "Kátia", "Leonardo", "Manuela", "Nuno", "Pamela", "Quirino", "Renata", "Silvio", "Tainá",
    "Uriel", "Viviane", "Waldir", "Xenia", "Yago", "Zara", "Aline", "Benício", "Cecília", "Dorian",
    "Eva", "Flávio", "Guilherme", "Hilda", "Ivan", "Júlia", "Kauã", "Lorena", "Marcos", "Nadia",
    "Osmar", "Priscila", "Quincy", "Roberto", "Sabrina", "Tadeu", "Vanessa", "Wilson", "Yuri", "Zilda",
    
    # Surnames to complete the list
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes",
    "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Mendes", "Rocha", "Pinto", "Freitas", "Barbosa",
    "Dias", "Fernandes", "Nunes", "Castro", "Moraes", "Pires", "Garcia", "Borges", "Machado", "Assis",
    "Azevedo", "Coelho", "Duarte", "Figueira", "Godoy", "Henriques", "Jardim", "Lopes", "Marques", "Neves",
    "Pacheco", "Quadros", "Ramires", "Santana", "Teixeira", "Viana", "Zanetti", "Andrade", "Barros", "Couto",
    "Esteves", "Fogaça", "Guedes", "Holanda", "Junqueira", "Lemos", "Magalhães", "Nascimento", "Ortiz", "Pupo",
    "Queiroz", "Rezende", "Soares", "Tavares", "Vieira", "Xavier", "Zimmermann", "Camargo", "Dantas", "Elias",
    "Faria", "Guerra", "Inácio", "Jordão", "Leal", "Medeiros", "Novaes", "Passos", "Quintana", "Ramos",
    "Sales", "Torres", "Uchoa", "Valente", "Ximenes", "Zacarias", "Batista", "Correia", "Fonseca", "Goulart"
]

def seed_database():
    """Inserts a large volume of test data (1000 clients and 2000 orders) into the database."""
    
    db = SessionLocal()
    objects_to_add = []
    
    try:
        print(f">>> Starting database seeding process for {NUM_CLIENTS} clients...")

        # --- 1. Generate 1000 Clients and 2000 Orders ---
        for i in range(1, NUM_CLIENTS + 1):
            client_id = i
            
            # Requested name generation logic (two random words)
            word1 = random.choice(WORD_LIST)
            word2 = random.choice(WORD_LIST)
            client_name = f"{word1} {word2}"

            client = ClientORM(id=client_id, name=client_name)
            objects_to_add.append(client)

            # Create two orders for each client
            order_1 = Order(number=f"ORD{client_id:04d}-A", client=client)
            order_2 = Order(number=f"ORD{client_id:04d}-B", client=client)
            
            objects_to_add.extend([order_1, order_2])

            if i % 100 == 0:
                print(f"    - Generated {i} clients...")


        # --- 2. Batch Insertion ---
        print(f">>> Inserting {len(objects_to_add)} records into the database...")
        db.add_all(objects_to_add)
        
        # --- 3. Commit Transaction ---
        db.commit()
        print(">>> Database seeding completed successfully.")
        print(f"  - Total Clients Inserted: {NUM_CLIENTS}")
        print(f"  - Total Orders Inserted: {NUM_CLIENTS * 2}")

    except Exception as e:
        db.rollback()
        print(f"!!! Error seeding the database. Rolling back transaction: {e}")
        print("Ensure the PostgreSQL server and the 'futino' database are running and accessible via .env.")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()