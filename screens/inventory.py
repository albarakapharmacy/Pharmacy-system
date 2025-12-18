from kivy.uix.screenmanager import Screen
from services.product_service import ProductService

class InventoryScreen(Screen):
    def load_products(self):
        products = ProductService.get_all()
        print(products)
        
        from services.barcode_service import BarcodeService

class InventoryScreen(Screen):
    def scan_barcode(self, image_path):
        code = BarcodeService.read_barcode(image_path)
        if code:
            print('BARCODE:', code)