import tkinter as tk
from tkinter import ttk

from database import Database
from product_manager import ProductManager
from sales_manager import SalesManager
from dashboard import Dashboard


class InventoryApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Inventory & Sales Management System"
        )

        self.root.geometry("1100x700")

        self.db = Database()

        self.create_tabs()

    # CREATE TABS

    def create_tabs(self):

        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(
            fill="both",
            expand=True
        )

        # Dashboard

        dashboard_tab = tk.Frame(
            self.notebook
        )

        self.notebook.add(
            dashboard_tab,
            text="Dashboard"
        )

        self.dashboard = Dashboard(
            dashboard_tab
        )

        # Products

        product_tab = tk.Frame(
            self.notebook
        )

        self.notebook.add(
            product_tab,
            text="Products"
        )

        self.product_manager = ProductManager(
            product_tab,
            self.refresh_all
        )

        # Sales


        sales_tab = tk.Frame(
            self.notebook
        )

        self.notebook.add(
            sales_tab,
            text="Sales"
        )

        self.sales_manager = SalesManager(
            sales_tab,
            self.refresh_all
        )


    # REFRESH EVERYTHING AUTOMATICALLY

    def refresh_all(self):

        # Update product table
        self.product_manager.load_products()

        # Update sales product list
        self.sales_manager.load_products()

        # Update dashboard
        self.dashboard.refresh_dashboard()


def main():

    root = tk.Tk()

    app = InventoryApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()