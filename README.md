# 🐍 Proxy Pattern Demo: Client and Orders (PostgreSQL/SQLAlchemy)

This project demonstrates the implementation of the **Virtual Proxy Pattern (Lazy Initialization)** in Python, using **SQLAlchemy** to simulate database access (PostgreSQL).  
The main goal is to control the loading of a high-cost domain object (`ClientORM`) only at the moment it is truly needed, improving performance.

---

## 📁 Project Structure

The source code is isolated within the `app/` package structure, following standard Python packaging practices.

```
/proxy-project
├── .env                  # PostgreSQL connection environment variables
├── requirements.txt      # Project dependencies
└── app/                  # Main Python Package
    ├── client.py         # Application Entry Point (GUI and Console Demo)
    ├── init_db.py        # Creates the Clients and Orders tables
    ├── cleanup_db.py     # **NEW:** Removes all tables (required for full reset)
    ├── seed_db.py        # **NEW:** Populates the DB with 1000 test clients
    └── src/
        ├── core/         # Domain Logic (Proxy, ORM Models)
        │   ├── client_proxy.py # The Virtual Proxy implementation
        │   ├── clientORM.py  # The Real Subject (SQLAlchemy Model)
        │   ├── model.py    # Database Configuration (Engine, Session)
        │   └── order.py    # Order Data Model
        └── gui/          # Presentation Layer (Tkinter App)
            └── client_gui.py
```

---

## 🛠️ Setup and Installation

### 1. Requirements
Ensure you have **Python 3.8+** installed and a **PostgreSQL server** running locally (default port 5432).

### 2. Environment Variables
Create or update the `.env` file inside the `app/` directory (`/proxy-project/app/.env`) with your database credentials:

```bash
# .env content example
DB_HOST=localhost
DB_PORT=5432
DB_NAME=futino
DB_USER=postgres
DB_PASSWORD=supra
DB_DRIVER=psycopg2
```

### 3. Python Dependencies
Install the necessary libraries using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

All scripts must be executed from the **project root directory** (`/proxy-project/`) using Python's **module notation** (`python -m`).

### 1. Initialize and Seed the Database

Before running the application, you must create the tables and insert the test data (1000 clients and 2000 orders).

| Command | Description |
|----------|-------------|
| `python -m app.init_db` | Creates the clients and orders tables in the database. |
| `python -m app.seed_db` | Inserts 1000 clients and 2000 orders (test data). *(Requires empty tables!)* |

**Data Cleanup (Required after "UniqueViolation" errors)**  
If you need to re-run `seed_db` after a duplicate key error, clear the tables using:

```bash
python -m app.cleanup_db
python -m app.init_db
python -m app.seed_db
```

---

### 2. Start the Demo Application

Execute the main entry point, which loads the graphical interface (**ClientApp / Tkinter**):

```bash
python -m app.client
```

When interacting with the GUI, observe the log (bottom part of the window) to see when the Proxy is:

- **Lazy Initializing:** Loading the `ClientORM` object from the database (only when you click *"Access Name"*).
- **Lazy Loading:** Fetching the list of orders via SQLAlchemy (only when you click *"Access Orders"*).
