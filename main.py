from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.inventory import InventoryScreen
from screens.sales import SalesScreen
from screens.reports import ReportsScreen
from screens.expiry import ExpiryScreen

class PharmacyApp(App):
    def build(self):
        Builder.load_file("pharmacy.kv")

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(InventoryScreen(name="inventory"))
        sm.add_widget(SalesScreen(name="sales"))
        sm.add_widget(ReportsScreen(name="reports"))
        sm.add_widget(ExpiryScreen(name="expiry"))
        return sm

if __name__ == "__main__":
    PharmacyApp().run()