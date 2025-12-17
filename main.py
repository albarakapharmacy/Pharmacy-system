import os
import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivy.utils import platform

# تحديد مسار قاعدة البيانات ليعمل على أندرويد
if platform == 'android':
    from android.storage import app_storage_path
    DB_PATH = os.path.join(app_storage_path(), 'pharmacy.db')
else:
    DB_PATH = 'pharmacy.db'

class DashboardScreen(Screen):
    # خصائص لتحديث الأرقام في الواجهة
    total_meds = StringProperty("0")
    today_sales = StringProperty("0")

    def on_enter(self):
        self.update_stats()

    def update_stats(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # جلب إحصائية بسيطة كمثال
        cur.execute("SELECT COUNT(*) FROM products")
        self.total_meds = str(cur.fetchone()[0])
        conn.close()

class InventoryScreen(Screen):
    products = ListProperty([])

    def on_enter(self):
        self.load_products()

    def load_products(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name, quantity, sale_price FROM products")
        self.products = cur.fetchall()
        conn.close()

class WindowManager(ScreenManager):
    pass

class PharmacyApp(App):
    def build(self):
        self.init_db()
        return WindowManager()

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # إنشاء الجداول الأساسية إذا لم تكن موجودة
        cur.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        quantity INTEGER,
                        sale_price REAL)''')
        conn.commit()
        conn.close()

if __name__ == '__main__':
    PharmacyApp().run()
