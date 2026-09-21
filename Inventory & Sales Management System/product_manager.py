import tkinter as tk
from tkinter import ttk, messagebox

from database import Database


class ProductManager:

    def __init__(self, parent, refresh_callback):

        self.parent = parent
        self.db = Database()
        self.refresh_callback = refresh_callback

        self.create_widgets()
        self.load_products()

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Product Management",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        # -------------------------
        # Input Frame
        # -------------------------

        input_frame = tk.Frame(self.parent)

        input_frame.pack(pady=10)

        # Product Name
        tk.Label(
            input_frame,
            text="Product Name"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.name_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        # Category
        tk.Label(
            input_frame,
            text="Category"
        ).grid(row=0, column=2, padx=5)

        self.category_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.category_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        # Price
        tk.Label(
            input_frame,
            text="Price"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.price_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.price_entry.grid(
            row=1,
            column=1,
            padx=5
        )

        # Quantity
        tk.Label(
            input_frame,
            text="Quantity"
        ).grid(row=1, column=2, padx=5)

        self.quantity_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.quantity_entry.grid(
            row=1,
            column=3,
            padx=5
        )

        # Minimum Stock
        tk.Label(
            input_frame,
            text="Minimum Stock"
        ).grid(row=2, column=0, padx=5, pady=5)

        self.min_stock_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.min_stock_entry.grid(
            row=2,
            column=1,
            padx=5
        )

        # -------------------------
        # Buttons
        # -------------------------

        button_frame = tk.Frame(self.parent)

        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Product",
            width=15,
            command=self.add_product
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update Product",
            width=15,
            command=self.update_product
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete Product",
            width=15,
            command=self.delete_product
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)

        # -------------------------
        # Product Table
        # -------------------------

        columns = (
            "ID",
            "Name",
            "Category",
            "Price",
            "Quantity",
            "Min Stock"
        )

        self.tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show="headings",
            height=15
        )

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=180)
        self.tree.column("Category", width=130)
        self.tree.column("Price", width=100)
        self.tree.column("Quantity", width=100)
        self.tree.column("Min Stock", width=100)

        self.tree.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_product
        )

    # -------------------------
    # Add Product
    # -------------------------

    def add_product(self):

        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        min_stock = self.min_stock_entry.get().strip()

        if not name or not category or not price or not quantity:

            messagebox.showwarning(
                "Input Error",
                "Please fill all required fields."
            )

            return

        try:

            price = float(price)
            quantity = int(quantity)

            if min_stock:
                min_stock = int(min_stock)
            else:
                min_stock = 5

            if price <= 0 or quantity < 0 or min_stock < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values."
            )

            return

        self.db.add_product(
            name,
            category,
            price,
            quantity,
            min_stock
        )

        messagebox.showinfo(
            "Success",
            "Product added successfully."
        )

        self.clear_fields()
        self.load_products()
        self.refresh_callback()

    # -------------------------
    # Load Products
    # -------------------------

    def load_products(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        products = self.db.get_products()

        for product in products:

            self.tree.insert(
                "",
                tk.END,
                values=product
            )

    # -------------------------
    # Select Product
    # -------------------------

    def select_product(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.clear_fields()

        self.name_entry.insert(
            0,
            values[1]
        )

        self.category_entry.insert(
            0,
            values[2]
        )

        self.price_entry.insert(
            0,
            values[3]
        )

        self.quantity_entry.insert(
            0,
            values[4]
        )

        self.min_stock_entry.insert(
            0,
            values[5]
        )

    # -------------------------
    # Update Product
    # -------------------------

    def update_product(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Error",
                "Please select a product."
            )

            return

        product_id = self.tree.item(
            selected[0],
            "values"
        )[0]

        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()

        try:

            price = float(
                self.price_entry.get()
            )

            quantity = int(
                self.quantity_entry.get()
            )

            min_stock = int(
                self.min_stock_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid values."
            )

            return

        self.db.update_product(
            product_id,
            name,
            category,
            price,
            quantity,
            min_stock
        )

        messagebox.showinfo(
            "Success",
            "Product updated successfully."
        )
        self.clear_fields()
        self.load_products()
        self.refresh_callback()
        

    # -------------------------
    # Delete Product
    # -------------------------

    def delete_product(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Error",
                "Please select a product."
            )

            return

        product_id = self.tree.item(
            selected[0],
            "values"
        )[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete selected product?"
        )

        if confirm:

            self.db.delete_product(
                product_id
            )

            messagebox.showinfo(
                "Success",
                "Product deleted successfully."
            )

            self.clear_fields()
            self.load_products()
            self.refresh_callback()
            

    # -------------------------
    # Clear Fields
    # -------------------------

    def clear_fields(self):

        self.name_entry.delete(
            0,
            tk.END
        )

        self.category_entry.delete(
            0,
            tk.END
        )

        self.price_entry.delete(
            0,
            tk.END
        )

        self.quantity_entry.delete(
            0,
            tk.END
        )

        self.min_stock_entry.delete(
            0,
            tk.END
        )