import matplotlib.pyplot as plt
import sqlite3

from database import Database


class Reports:

    def __init__(self):

        self.db = Database()

    def category_sales_report(self):

        connection = self.db.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                p.category,
                SUM(si.quantity * si.price)
            FROM sale_items si
            JOIN products p
                ON si.product_id = p.id
            GROUP BY p.category
        """)

        data = cursor.fetchall()

        connection.close()

        if not data:

            print("No sales data available.")

            return

        categories = [
            row[0]
            for row in data
        ]

        amounts = [
            row[1]
            for row in data
        ]

        plt.figure(
            figsize=(8, 6)
        )

        plt.bar(
            categories,
            amounts
        )

        plt.title(
            "Category-wise Sales"
        )

        plt.xlabel(
            "Category"
        )

        plt.ylabel(
            "Sales Amount"
        )

        plt.xticks(
            rotation=30
        )

        plt.tight_layout()

        plt.show()