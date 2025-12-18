from db.database import Database
from datetime import datetime

class SalesService:
    @staticmethod
    def create_sale(items):
        db = Database()
        total = sum(i['qty'] * i['price'] for i in items)

        db.execute(
            'INSERT INTO sales (date, total) VALUES (?, ?)',
            (datetime.now().strftime('%Y-%m-%d %H:%M'), total)
        )
        sale_id = db.cursor.lastrowid

        for i in items:
            db.execute(
                'INSERT INTO sale_items (sale_id, product_id, qty, price) VALUES (?,?,?,?)',
                (sale_id, i['product_id'], i['qty'], i['price'])
            )

        return sale_id, total