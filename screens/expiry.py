from kivy.uix.screenmanager import Screen
from services.expiry_service import ExpiryService

class ExpiryScreen(Screen):
    def load_alerts(self):
        expired = ExpiryService.expired_products()
        near = ExpiryService.near_expiry()
        low = ExpiryService.low_stock()

        print('Expired:', expired)
        print('Near Expiry:', near)
        print('Low Stock:', low)