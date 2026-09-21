import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import Database


class SalesManager:

    def __init__(
        self,
        parent,
        refresh_callback
    ):

        self.parent = parent

        self.db = Database()

        self.refresh_callback = refresh_callback

        self.products = []

        self.cart = []

        self.create_widgets()

        self.load_products()

    # ==========================================
    # CREATE WIDGETS
    # ==========================================

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Sales Management",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        # ======================================
        # SEARCH FRAME
        # ======================================

        search_frame = tk.Frame(
            self.parent
        )

        search_frame.pack(
            pady=10
        )

        # Search

        tk.Label(
            search_frame,
            text="Search Product:"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_product
        )

        # Product dropdown

        tk.Label(
            search_frame,
            text="Select Product:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.product_combo = ttk.Combobox(
            search_frame,
            width=30,
            state="readonly"
        )

        self.product_combo.grid(
            row=0,
            column=3,
            padx=5
        )

        # Quantity

        tk.Label(
            search_frame,
            text="Quantity:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=10
        )

        self.quantity_entry = tk.Entry(
            search_frame,
            width=10
        )

        self.quantity_entry.grid(
            row=1,
            column=1,
            padx=5
        )

        # Add button

        tk.Button(
            search_frame,
            text="Add to Cart",
            width=15,
            command=self.add_to_cart
        ).grid(
            row=1,
            column=3,
            padx=5
        )

        # ======================================
        # CART
        # ======================================

        columns = (
            "Product",
            "Price",
            "Quantity",
            "Total"
        )

        self.cart_tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show="headings",
            height=12
        )

        for column in columns:

            self.cart_tree.heading(
                column,
                text=column
            )

        self.cart_tree.column(
            "Product",
            width=250
        )

        self.cart_tree.column(
            "Price",
            width=120
        )

        self.cart_tree.column(
            "Quantity",
            width=100
        )

        self.cart_tree.column(
            "Total",
            width=150
        )

        self.cart_tree.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        # ======================================
        # TOTAL
        # ======================================

        self.total_label = tk.Label(
            self.parent,
            text="Total Sales: ₹0.00",
            font=("Arial", 16, "bold")
        )

        self.total_label.pack(
            pady=10
        )

        # ======================================
        # COMPLETE SALE
        # ======================================

        tk.Button(
            self.parent,
            text="Complete Sale",
            width=20,
            command=self.complete_sale
        ).pack(
            pady=10
        )

    # ==========================================
    # LOAD PRODUCTS
    # ==========================================

    def load_products(self):

        self.products = (
            self.db.get_products()
        )

        product_names = []

        for product in self.products:

            product_names.append(
                f"{product[0]} - {product[1]}"
            )

        self.product_combo["values"] = (
            product_names
        )

    # ==========================================
    # SEARCH PRODUCT
    # ==========================================

    def search_product(self, event=None):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        filtered_products = []

        for product in self.products:

            product_id = product[0]

            product_name = product[1]

            if search_text in product_name.lower():

                filtered_products.append(
                    f"{product_id} - {product_name}"
                )

        self.product_combo["values"] = (
            filtered_products
        )

        if filtered_products:

            self.product_combo.event_generate(
                "<Down>"
            )

    # ==========================================
    # ADD TO CART
    # ==========================================

    def add_to_cart(self):

        selected = (
            self.product_combo.get()
        )

        quantity_text = (
            self.quantity_entry.get()
        )

        if not selected:

            messagebox.showwarning(
                "Product Required",
                "Please select a product."
            )

            return

        try:

            quantity = int(
                quantity_text
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Enter a valid quantity."
            )

            return

        product_id = int(
            selected.split(" - ")[0]
        )

        product = self.db.get_product(
            product_id
        )

        if product is None:

            messagebox.showerror(
                "Error",
                "Product not found."
            )

            return

        name = product[1]

        price = product[3]

        stock = product[4]

        if quantity > stock:

            messagebox.showerror(
                "Insufficient Stock",
                f"Only {stock} units available."
            )

            return

        # Check existing cart item

        for item in self.cart:

            if item["product_id"] == product_id:

                new_quantity = (
                    item["quantity"] + quantity
                )

                if new_quantity > stock:

                    messagebox.showerror(
                        "Insufficient Stock",
                        f"Only {stock} units available."
                    )

                    return

                item["quantity"] = (
                    new_quantity
                )

                item["total"] = (
                    new_quantity * price
                )

                self.refresh_cart()

                self.clear_selection()

                return

        # Add new item

        total = price * quantity

        self.cart.append({
            "product_id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "total": total
        })

        self.refresh_cart()

        self.clear_selection()

    # ==========================================
    # REFRESH CART
    # ==========================================

    def refresh_cart(self):

        for item in self.cart_tree.get_children():

            self.cart_tree.delete(item)

        total_amount = 0

        for item in self.cart:

            self.cart_tree.insert(
                "",
                tk.END,
                values=(
                    item["name"],
                    f"₹{item['price']:.2f}",
                    item["quantity"],
                    f"₹{item['total']:.2f}"
                )
            )

            total_amount += item["total"]

        self.total_label.config(
            text=f"Total Sales: ₹{total_amount:.2f}"
        )

    # ==========================================
    # CLEAR SELECTION
    # ==========================================

    def clear_selection(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.product_combo.set("")

        self.quantity_entry.delete(
            0,
            tk.END
        )

        self.load_products()

    # ==========================================
    # COMPLETE SALE
    # ==========================================

    def complete_sale(self):

        if not self.cart:

            messagebox.showwarning(
                "Empty Cart",
                "Please add products to the cart."
            )

            return

        total = sum(
            item["total"]
            for item in self.cart
        )

        sale_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Create sale record

        sale_id = self.db.create_sale(
            sale_date,
            total
        )

        # Save sale items

        for item in self.cart:

            self.db.add_sale_item(
                sale_id,
                item["product_id"],
                item["quantity"],
                item["price"]
            )

            # Reduce stock

            self.db.update_stock(
                item["product_id"],
                -item["quantity"]
            )

        # Success message

        messagebox.showinfo(
            "Sale Completed",
            f"Sale ID: {sale_id}\n"
            f"Total Amount: ₹{total:.2f}"
        )

        # Clear cart

        self.cart = []

        self.refresh_cart()

        self.clear_selection()

        # ======================================
        # AUTOMATICALLY UPDATE ENTIRE APPLICATION
        # ======================================

        self.refresh_callback()