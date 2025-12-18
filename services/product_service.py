from db.database import Database

class ProductService:
    @staticmethod
    def add(name, barcode, price, qty, expiry):
        db = Database()
        db.execute(
            'INSERT INTO products (name, barcode, price, quantity, expiry) VALUES (?,?,?,?,?)',
            (name, barcode, price, qty, expiry)
        )

    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all('SELECT * FROM products')

from db.database import Database

class ProductService:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM products")
        
        from services.product_service import ProductService

class InventoryScreen(Screen):
    def load_products(self):
        products = ProductService.get_all()
        for p in products:
            print(p)