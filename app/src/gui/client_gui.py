import tkinter as tk
from tkinter import ttk, messagebox
import sys
import io

try:
    from app.src.core.client_proxy import ClientProxy
except ImportError:
    messagebox.showerror("Import Error", 
                         "Ensure that 'client_proxy.py', 'model.py', 'clientORM.py', and 'order.py' files are in the same directory.")
    sys.exit()

class ClientApp(tk.Tk):
    """
    Graphical interface to demonstrate the ClientProxy and the Lazy Loading pattern.
    """
    def __init__(self):
        super().__init__()
        self.title("Proxy Pattern Demo - Client Manager")
        self.geometry("600x650")
        
        self.client_proxy = None
        self.current_client_id = tk.StringVar()
        self.client_name_var = tk.StringVar(value="No Client Loaded")
        self.new_order_number_var = tk.StringVar()

        # Configure the redirection of standard output (stdout) to the log widget
        self._setup_logging()
        
        self._create_widgets()

        # Configure the window closing handler to close the DB connection
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_logging(self):
        """Redirects console output (stdout) to the log widget in the GUI."""
        self.log_text = None
        self.stdout_orig = sys.stdout
        self.log_io = io.StringIO()
        sys.stdout = self.log_io

    def _update_log_display(self):
        """Updates the log widget with new messages from stdout."""
        if self.log_text:
            content = self.log_io.getvalue()
            self.log_text.delete('1.0', tk.END)
            self.log_text.insert(tk.END, content)
            self.log_text.see(tk.END) # Scroll to the end
            # Clear the log_io buffer after display
            self.log_io.seek(0)
            self.log_io.truncate(0)

    def _create_widgets(self):
        """Creates and organizes all interface widgets."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Section 1: Load Client (Lazy Initialization)
        load_frame = ttk.LabelFrame(main_frame, text="1. Load Client (Virtual Proxy)", padding="10")
        load_frame.pack(fill="x", pady=10)

        ttk.Label(load_frame, text="Client ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(load_frame, textvariable=self.current_client_id, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Button to initiate client loading
        ttk.Button(load_frame, text="Access Name (Triggers Lazy Initialization)", command=self.load_client_name).grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Label(load_frame, text="Client Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(load_frame, textvariable=self.client_name_var, foreground="blue", font=('Arial', 10, 'bold')).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Section 2: View Orders (Lazy Loading)
        orders_frame = ttk.LabelFrame(main_frame, text="2. View Orders (Lazy Loading)", padding="10")
        orders_frame.pack(fill="x", pady=10)

        ttk.Button(orders_frame, text="Access Orders (Triggers Lazy Loading)", command=self.view_orders).pack(pady=10)
        
        self.orders_listbox = tk.Listbox(orders_frame, height=5)
        self.orders_listbox.pack(fill="x", expand=True)

        # Section 3: Add Order
        add_frame = ttk.LabelFrame(main_frame, text="3. Add New Order", padding="10")
        add_frame.pack(fill="x", pady=10)

        ttk.Label(add_frame, text="Order Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(add_frame, textvariable=self.new_order_number_var, width=20).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Button(add_frame, text="Add Order", command=self.add_new_order).grid(row=1, column=0, columnspan=2, pady=10)

        # Section 4: Output Log
        log_frame = ttk.LabelFrame(main_frame, text="4. Console Log (Demonstrates Lazy Loading/Initialization)", padding="10")
        log_frame.pack(fill="both", expand=True, pady=10)

        self.log_text = tk.Text(log_frame, height=10, state='normal', bg='light grey', fg='black')
        self.log_text.pack(fill="both", expand=True)
        self.log_io.write("Waiting for Client ID and actions...\n")
        self._update_log_display()

    def _reset_state(self):
        """Clears the application state and closes the previous connection."""
        if self.client_proxy:
            self.client_proxy.close() # Ensures the old session is closed
            self.client_proxy = None
        
        # Clear the log and state variables
        self.log_io.seek(0)
        self.log_io.truncate(0)
        self.log_io.write("Waiting for Client ID and actions...\n")
        
        self.client_name_var.set("No Client Loaded")
        self.orders_listbox.delete(0, tk.END)
        self._update_log_display()

    def load_client_name(self):
        """
        Accesses the 'name' property, which triggers Lazy Initialization 
        (loading of the client).
        """
        client_id_str = self.current_client_id.get().strip()
        if not client_id_str.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid numeric Client ID.")
            return

        client_id = int(client_id_str)
        self._reset_state()
        
        try:
            # 1. Instantiate the Proxy (Does not access the DB yet)
            self.client_proxy = ClientProxy(client_id=client_id)
            self.log_io.write(f">>> [GUI] ClientProxy({client_id}) instantiated.\n")
            
            # 2. Access the 'name' property (Triggers Lazy Initialization)
            client_name = self.client_proxy.name
            
            self.client_name_var.set(client_name)
            self.log_io.write(f">>> [GUI] Client Name: {client_name}\n")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.client_name_var.set("Client not found!")
            self._reset_state()
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection/Operation failure: {e}")
            self._reset_state()
        finally:
            self._update_log_display()


    def view_orders(self):
        """
        Accesses the 'orders' property, which triggers Lazy Loading of orders.
        """
        if not self.client_proxy:
            messagebox.showwarning("Warning", "First, load a client (use the 'Access Name' button).")
            return
        
        self.orders_listbox.delete(0, tk.END)

        try:
            # Access the 'orders' property (Triggers Lazy Loading)
            orders = self.client_proxy.orders
            
            if orders:
                for i, order in enumerate(orders):
                    self.orders_listbox.insert(tk.END, f"ID: {order.id} | Number: {order.number}")
                self.log_io.write(f">>> [GUI] {len(orders)} orders loaded into the list.\n")
            else:
                self.orders_listbox.insert(tk.END, "No orders found.")
                self.log_io.write(">>> [GUI] No orders found.\n")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders: {e}")
        finally:
            self._update_log_display()


    def add_new_order(self):
        """
        Adds a new order, using the real client object through the Proxy.
        """
        if not self.client_proxy:
            messagebox.showwarning("Warning", "First, load a client (use the 'Access Name' button).")
            return

        order_number = self.new_order_number_var.get().strip()
        if not order_number:
            messagebox.showerror("Input Error", "Please enter an Order Number.")
            return

        try:
            # The Proxy delegates the persistence action to the real object
            self.client_proxy.add_order(order_number)
            self.new_order_number_var.set("") # Clear the input field
            
            # Automatically update the orders list after insertion
            self.view_orders() 

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add order: {e}")
        finally:
            self._update_log_display()


    def on_closing(self):
        """Closes the database connection before shutting down the application."""
        if self.client_proxy:
            self.client_proxy.close()
            print(">>> [GUI] Database connection closed (ClientProxy.close()).")
            self._update_log_display()

        # Restore the original standard output
        sys.stdout = self.stdout_orig
        
        self.destroy()

