import tkinter as tk
from tkinter import ttk

from database import Database


class Dashboard:

    def __init__(self, parent):

        self.parent = parent
        self.db = Database()

        self.create_dashboard()

    # ==========================================
    # CREATE DASHBOARD
    # ==========================================

    def create_dashboard(self):

        title = tk.Label(
            self.parent,
            text="Inventory Dashboard",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)

        # ======================================
        # CARDS
        # ======================================

        self.cards_frame = tk.Frame(
            self.parent
        )

        self.cards_frame.pack(pady=20)

        self.total_products_label = self.create_card(
            "Total Products",
            0
        )

        self.total_stock_label = self.create_card(
            "Total Stock",
            1
        )

        self.total_sales_label = self.create_card(
            "Total Sales",
            2
        )

        

        self.low_stock_label = self.create_card(
            "Lowest Stock Product",
            3
        )

        # ======================================
        # TABLE TITLE
        # ======================================

        tk.Label(
            self.parent,
            text="All Products",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ======================================
        # ALL PRODUCTS TABLE
        # ======================================

        table_frame = tk.Frame(
            self.parent
        )

        table_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        columns = (
            "Product ID",
            "Product",
            "Category",
            "Price",
            "Quantity",
            "Minimum Stock"
        )

        self.product_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Headings

        for column in columns:

            self.product_tree.heading(
                column,
                text=column
            )

        # Column widths

        self.product_tree.column(
            "Product ID",
            width=100,
            anchor="center"
        )

        self.product_tree.column(
            "Product",
            width=200,
            anchor="center"
        )

        self.product_tree.column(
            "Category",
            width=150,
            anchor="center"
        )

        self.product_tree.column(
            "Price",
            width=120,
            anchor="center"
        )

        self.product_tree.column(
            "Quantity",
            width=120,
            anchor="center"
        )

        self.product_tree.column(
            "Minimum Stock",
            width=150,
            anchor="center"
        )

        self.product_tree.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # INITIAL REFRESH
        # ======================================

        self.refresh_dashboard()

    # ==========================================
    # CREATE CARD
    # ==========================================

    def create_card(
        self,
        title,
        column
    ):

        card = tk.Frame(
            self.cards_frame,
            borderwidth=2,
            relief="groove",
            padx=25,
            pady=20
        )

        card.grid(
            row=0,
            column=column,
            padx=10
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 12)
        ).pack()

        value_label = tk.Label(
            card,
            text="0",
            font=("Arial", 16, "bold"),
            wraplength=180
        )

        value_label.pack(
            pady=10
        )

        return value_label

    # ==========================================
    # REFRESH DASHBOARD
    # ==========================================

    def refresh_dashboard(self):

        # ======================================
        # TOTAL PRODUCTS
        # ======================================

        total_products = (
            self.db.get_total_products()
        )

        self.total_products_label.config(
            text=str(total_products)
        )

        # ======================================
        # TOTAL STOCK
        # ======================================

        total_stock = (
            self.db.get_total_stock()
        )

        self.total_stock_label.config(
            text=str(total_stock)
        )

        # ======================================
        # TOTAL SALES
        # ======================================

        total_sales = (
            self.db.get_total_sales()
        )

        self.total_sales_label.config(
            text=f"₹{total_sales:.2f}"
        )

        # ======================================
        # GET ALL PRODUCTS
        # ======================================

        products = self.db.get_products()

        # ======================================
        # LOWEST STOCK PRODUCT
        # ======================================

        if products:

            lowest_product = min(
                products,
                key=lambda product: product[4]
            )

            product_id = lowest_product[0]
            product_name = lowest_product[1]
            quantity = lowest_product[4]

            self.low_stock_label.config(
                text=f"ID: {product_id}\n"
                     f"{product_name}\n"
                     f"Qty: {quantity}"
            )

        else:

            self.low_stock_label.config(
                text="No Products"
            )

        # ======================================
        # CLEAR OLD PRODUCT TABLE
        # ======================================

        for item in self.product_tree.get_children():

            self.product_tree.delete(
                item
            )

        # ======================================
        # SHOW ALL PRODUCTS
        # ======================================

        for product in products:

            product_id = product[0]
            product_name = product[1]
            category = product[2]
            price = product[3]
            quantity = product[4]
            minimum_stock = product[5]

            self.product_tree.insert(
                "",
                tk.END,
                values=(
                    product_id,
                    product_name,
                    category,
                    f"₹{price:.2f}",
                    quantity,
                    minimum_stock
                )
            )