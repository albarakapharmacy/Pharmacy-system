from db.database import Database
from datetime import datetime, timedelta

class ExpiryService:
    @staticmethod
    def expired_products():
        today = datetime.now().date()
        db = Database()
        return db.fetch_all(
            'SELECT * FROM products WHERE expiry < ?',
            (today,)
        )

    @staticmethod
    def near_expiry(days=30):
        today = datetime.now().date()
        limit = today + timedelta(days=days)
        db = Database()
        return db.fetch_all(
            'SELECT * FROM products WHERE expiry BETWEEN ? AND ?',
            (today, limit)
        )

    @staticmethod
    def low_stock(threshold=5):
        db = Database()
        return db.fetch_all(
            'SELECT * FROM products WHERE quantity <= ?',
            (threshold,)
        )