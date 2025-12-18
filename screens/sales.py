from kivy.uix.screenmanager import Screen
from services.sales_service import SalesService

class SalesScreen(Screen):
    cart = []

    def add_to_cart(self, product):
        self.cart.append(product)

    def save_invoice(self):
        sale_id, total = SalesService.create_sale(self.cart)
        print('Invoice saved:', sale_id, total)
        self.cart = []