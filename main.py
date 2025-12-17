import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
from datetime import datetime, timedelta
import csv
import os
from tkcalendar import DateEntry

class PharmacyInventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام إدارة مخزون صيدلية البركة")
        self.root.geometry("1400x800")
        
        # إعداد قاعدة البيانات
        self.setup_database()
        
        # إعداد الواجهة
        self.setup_ui()
        
        # تحميل البيانات الأولية
        self.load_data()
        
    def setup_database(self):
        """إعداد قاعدة البيانات SQLite"""
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        
        # إنشاء الجداول
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                barcode TEXT,
                                name TEXT NOT NULL,
                                unit TEXT,
                                type TEXT,
                                manufacturer TEXT,
                                purchase_price REAL,
                                sale_price REAL,
                                quantity INTEGER,
                                min_stock INTEGER DEFAULT 10,
                                expiry_date DATE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                age INTEGER,
                                phone TEXT,
                                diagnosis TEXT,
                                last_visit DATE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                code TEXT,
                                name TEXT NOT NULL,
                                specialty TEXT,
                                phone TEXT,
                                email TEXT,
                                address TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                invoice_number TEXT UNIQUE,
                                date DATE NOT NULL,
                                patient_name TEXT,
                                total_amount REAL,
                                payment_method TEXT,
                                items TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                prescription_number TEXT UNIQUE,
                                date DATE NOT NULL,
                                patient_name TEXT,
                                doctor_name TEXT,
                                drugs TEXT,
                                status TEXT DEFAULT 'معلقة',
                                notes TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
        
        self.conn.commit()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # إنشاء Notebook للتبويب
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # إنشاء الألسنة المختلفة
        self.create_dashboard_tab()
        self.create_inventory_tab()
        self.create_customers_tab()
        self.create_suppliers_tab()
        self.create_sales_tab()
        self.create_prescriptions_tab()
        self.create_expiry_tab()
        self.create_reports_tab()
        
        # شريط الحالة
        self.status_bar = tk.Label(self.root, text="جاهز", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # تحديث شريط الحالة بالتاريخ
        self.update_status_bar()
        
    def update_status_bar(self):
        """تحديث شريط الحالة بالتاريخ والوقت"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar.config(text=f"التاريخ: {date_str} | صيدلاني: ادريس سلطان")
        self.root.after(1000, self.update_status_bar)
        
    def create_dashboard_tab(self):
        """إنشاء لسان لوحة التحكم"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text='لوحة التحكم')
        
        # عناوين
        title_label = ttk.Label(dashboard_frame, text="لوحة تحكم الصيدلية", 
                                font=('Arial', 20, 'bold'))
        title_label.pack(pady=10)
        
        # إطار للإحصائيات
        stats_frame = ttk.Frame(dashboard_frame)
        stats_frame.pack(pady=10, padx=10, fill='x')
        
        # بطاقات الإحصائيات
        self.create_stat_card(stats_frame, "إجمالي الأدوية", "0", 0, "fas fa-capsules")
        self.create_stat_card(stats_frame, "فواتير اليوم", "0", 1, "fas fa-receipt")
        self.create_stat_card(stats_frame, "المرضى المسجلين", "0", 2, "fas fa-user-injured")
        self.create_stat_card(stats_frame, "أدوية قريبة الانتهاء", "0", 3, "fas fa-exclamation-triangle")
        
        # تنبيهات المخزون
        alert_frame = ttk.LabelFrame(dashboard_frame, text="تنبيهات المخزون", padding=10)
        alert_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # شجرة لعرض التنبيهات
        columns = ("الدواء", "الكمية المتاحة", "الحد الأدنى", "تاريخ الانتهاء", "الحالة")
        self.alert_tree = ttk.Treeview(alert_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.alert_tree.heading(col, text=col)
            self.alert_tree.column(col, width=150)
            
        scrollbar = ttk.Scrollbar(alert_frame, orient="vertical", command=self.alert_tree.yview)
        self.alert_tree.configure(yscrollcommand=scrollbar.set)
        
        self.alert_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
    def create_stat_card(self, parent, title, value, column, icon):
        """إنشاء بطاقة إحصائية"""
        card_frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=2)
        card_frame.grid(row=0, column=column, padx=5, pady=5, sticky='nsew')
        
        # جعل الأعمدة متساوية الحجم
        parent.grid_columnconfigure(column, weight=1)
        
        # العنوان
        title_label = ttk.Label(card_frame, text=title, font=('Arial', 12))
        title_label.pack(pady=(10, 5))
        
        # القيمة
        value_label = ttk.Label(card_frame, text=value, font=('Arial', 24, 'bold'))
        value_label.pack(pady=5)
        
        # الرمز (محاكاة باستخدام نص)
        icon_label = ttk.Label(card_frame, text="📊", font=('Arial', 30))
        icon_label.pack(pady=10)
        
        return value_label
        
    def create_inventory_tab(self):
        """إنشاء لسان الأدوية والمستلزمات"""
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text='الأدوية والمستلزمات')
        
        # شريط الأدوات
        toolbar = ttk.Frame(inventory_frame)
        toolbar.pack(fill='x', pady=5)
        
        ttk.Button(toolbar, text="إضافة دواء جديد", 
                  command=self.add_product_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="استيراد من Excel", 
                  command=self.import_from_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="تصدير إلى Excel", 
                  command=self.export_to_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="حذف المنتجات", 
                  command=self.delete_all_products).pack(side=tk.LEFT, padx=5)
        
        # شجرة لعرض المنتجات
        columns = ("الباركود", "اسم الدواء", "الوحدة", "الشكل الصيدلاني", 
                  "الشركة المصنعة", "سعر الشراء", "سعر البيع", 
                  "الكمية", "تاريخ الانتهاء", "الإجراءات")
        
        self.product_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=120)
            
        # إضافة أشرطة التمرير
        scrollbar_y = ttk.Scrollbar(inventory_frame, orient="vertical", command=self.product_tree.yview)
        scrollbar_x = ttk.Scrollbar(inventory_frame, orient="horizontal", command=self.product_tree.xview)
        self.product_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.product_tree.pack(side=tk.TOP, fill='both', expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill='y')
        scrollbar_x.pack(side=tk.BOTTOM, fill='x')
        
        # ربط حدث النقر المزدوج
        self.product_tree.bind('<Double-1>', self.on_product_double_click)
        
    def create_customers_tab(self):
        """إنشاء لسان المرضى والعملاء"""
        customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(customers_frame, text='المرضى والعملاء')
        
        # شريط الأدوات
        toolbar = ttk.Frame(customers_frame)
        toolbar.pack(fill='x', pady=5)
        
        ttk.Button(toolbar, text="إضافة مريض جديد", 
                  command=self.add_customer_dialog).pack(side=tk.LEFT, padx=5)
        
        # شجرة لعرض العملاء
        columns = ("رقم المريض", "اسم المريض", "العمر", "الهاتف", 
                  "التشخيص / الأمراض", "آخر زيارة", "الإجراءات")
        
        self.customer_tree = ttk.Treeview(customers_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=120)
            
        scrollbar_y = ttk.Scrollbar(customers_frame, orient="vertical", command=self.customer_tree.yview)
        scrollbar_x = ttk.Scrollbar(customers_frame, orient="horizontal", command=self.customer_tree.xview)
        self.customer_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.customer_tree.pack(side=tk.TOP, fill='both', expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill='y')
        scrollbar_x.pack(side=tk.BOTTOM, fill='x')
        
    def create_suppliers_tab(self):
        """إنشاء لسان الموردين"""
        suppliers_frame = ttk.Frame(self.notebook)
        self.notebook.add(suppliers_frame, text='الموردين')
        
        # شريط الأدوات
        toolbar = ttk.Frame(suppliers_frame)
        toolbar.pack(fill='x', pady=5)
        
        ttk.Button(toolbar, text="إضافة مورد جديد", 
                  command=self.add_supplier_dialog).pack(side=tk.LEFT, padx=5)
        
        # شجرة لعرض الموردين
        columns = ("كود المورد", "اسم المورد", "التخصص", "الهاتف", 
                  "البريد الإلكتروني", "العنوان", "الإجراءات")
        
        self.supplier_tree = ttk.Treeview(suppliers_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.supplier_tree.heading(col, text=col)
            self.supplier_tree.column(col, width=120)
            
        scrollbar = ttk.Scrollbar(suppliers_frame, orient="vertical", command=self.supplier_tree.yview)
        self.supplier_tree.configure(yscrollcommand=scrollbar.set)
        
        self.supplier_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
    def create_sales_tab(self):
        """إنشاء لسان فواتير الصرف"""
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text='فواتير الصرف')
        
        # شريط الأدوات
        toolbar = ttk.Frame(sales_frame)
        toolbar.pack(fill='x', pady=5)
        
        ttk.Button(toolbar, text="فاتورة صرف جديدة", 
                  command=self.add_sales_invoice_dialog).pack(side=tk.LEFT, padx=5)
        
        # شجرة لعرض الفواتير
        columns = ("رقم الفاتورة", "التاريخ", "اسم المريض", 
                  "إجمالي الفاتورة", "طريقة الدفع", "الإجراءات")
        
        self.sales_tree = ttk.Treeview(sales_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=150)
            
        scrollbar = ttk.Scrollbar(sales_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
    def create_prescriptions_tab(self):
        """إنشاء لسان الوصفات الطبية"""
        prescriptions_frame = ttk.Frame(self.notebook)
        self.notebook.add(prescriptions_frame, text='الوصفات الطبية')
        
        # شريط الأدوات
        toolbar = ttk.Frame(prescriptions_frame)
        toolbar.pack(fill='x', pady=5)
        
        ttk.Button(toolbar, text="إضافة وصفة جديدة", 
                  command=self.add_prescription_dialog).pack(side=tk.LEFT, padx=5)
        
        # شجرة لعرض الوصفات
        columns = ("رقم الوصفة", "التاريخ", "اسم المريض", "اسم الطبيب", 
                  "عدد الأدوية", "الحالة", "الإجراءات")
        
        self.prescription_tree = ttk.Treeview(prescriptions_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.prescription_tree.heading(col, text=col)
            self.prescription_tree.column(col, width=120)
            
        scrollbar = ttk.Scrollbar(prescriptions_frame, orient="vertical", command=self.prescription_tree.yview)
        self.prescription_tree.configure(yscrollcommand=scrollbar.set)
        
        self.prescription_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
    def create_expiry_tab(self):
        """إنشاء لسان الأدوية منتهية الصلاحية"""
        expiry_frame = ttk.Frame(self.notebook)
        self.notebook.add(expiry_frame, text='منتهية الصلاحية')
        
        # شجرة لعرض الأدوية المنتهية
        columns = ("اسم الدواء", "الكمية المتاحة", "تاريخ الانتهاء", 
                  "الأيام المتبقية", "سعر الشراء", "القيمة الإجمالية", "الإجراءات")
        
        self.expiry_tree = ttk.Treeview(expiry_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.expiry_tree.heading(col, text=col)
            self.expiry_tree.column(col, width=150)
            
        scrollbar = ttk.Scrollbar(expiry_frame, orient="vertical", command=self.expiry_tree.yview)
        self.expiry_tree.configure(yscrollcommand=scrollbar.set)
        
        self.expiry_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
    def create_reports_tab(self):
        """إنشاء لسان التقارير"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text='التقارير')
        
        # إطار عوامل التصفية
        filter_frame = ttk.LabelFrame(reports_frame, text="معايير التقرير", padding=10)
        filter_frame.pack(fill='x', pady=5, padx=5)
        
        ttk.Label(filter_frame, text="نوع التقرير:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.report_type = ttk.Combobox(filter_frame, values=["تقرير المبيعات", "تقرير المخزون", 
                                                           "تقرير الأدوية المنتهية", "تقرير المرضى",
                                                           "تقرير الوصفات الطبية"])
        self.report_type.grid(row=0, column=1, padx=5, pady=5)
        self.report_type.current(0)
        
        ttk.Label(filter_frame, text="من تاريخ:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.report_from_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.report_from_date.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="إلى تاريخ:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.report_to_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.report_to_date.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(filter_frame, text="توليد التقرير", 
                  command=self.generate_report).grid(row=0, column=6, padx=5, pady=5)
        
        # شجرة لعرض التقرير
        columns = ("التاريخ", "البيان", "الكمية", "القيمة", "الإجمالي")
        
        self.report_tree = ttk.Treeview(reports_frame, columns=columns, show='headings', height=25)
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=200)
            
        scrollbar = ttk.Scrollbar(reports_frame, orient="vertical", command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        
        self.report_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
    def load_data(self):
        """تحميل البيانات من قاعدة البيانات"""
        # تحميل المنتجات
        self.load_products()
        
        # تحميل العملاء
        self.load_customers()
        
        # تحميل الموردين
        self.load_suppliers()
        
        # تحميل الفواتير
        self.load_sales()
        
        # تحميل الوصفات
        self.load_prescriptions()
        
        # تحديث لوحة التحكم
        self.update_dashboard()
        
        # تحميل الأدوية المنتهية
        self.load_expiry_products()
        
    def load_products(self):
        """تحميل المنتجات وعرضها"""
        self.product_tree.delete(*self.product_tree.get_children())
        
        self.cursor.execute("SELECT * FROM products ORDER BY name")
        products = self.cursor.fetchall()
        
        for product in products:
            self.product_tree.insert('', 'end', values=(
                product[1], product[2], product[3], product[4], product[5],
                f"{product[6]:.2f}", f"{product[7]:.2f}", product[8],
                product[10], "تعديل/حذف"
            ), iid=product[0])
            
    def load_customers(self):
        """تحميل العملاء وعرضهم"""
        self.customer_tree.delete(*self.customer_tree.get_children())
        
        self.cursor.execute("SELECT * FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        
        for customer in customers:
            self.customer_tree.insert('', 'end', values=(
                customer[0], customer[1], customer[2], customer[3],
                customer[4], customer[5], "تعديل/حذف"
            ), iid=customer[0])
            
    def load_suppliers(self):
        """تحميل الموردين وعرضهم"""
        self.supplier_tree.delete(*self.supplier_tree.get_children())
        
        self.cursor.execute("SELECT * FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        
        for supplier in suppliers:
            self.supplier_tree.insert('', 'end', values=(
                supplier[1], supplier[2], supplier[3], supplier[4],
                supplier[5], supplier[6], "تعديل/حذف"
            ), iid=supplier[0])
            
    def load_sales(self):
        """تحميل الفواتير وعرضها"""
        self.sales_tree.delete(*self.sales_tree.get_children())
        
        self.cursor.execute("SELECT * FROM sales ORDER BY date DESC")
        sales = self.cursor.fetchall()
        
        for sale in sales:
            self.sales_tree.insert('', 'end', values=(
                sale[1], sale[2], sale[3], f"{sale[4]:.2f}",
                sale[5], "عرض/حذف"
            ), iid=sale[0])
            
    def load_prescriptions(self):
        """تحميل الوصفات وعرضها"""
        self.prescription_tree.delete(*self.prescription_tree.get_children())
        
        self.cursor.execute("SELECT * FROM prescriptions ORDER BY date DESC")
        prescriptions = self.cursor.fetchall()
        
        for pres in prescriptions:
            # حساب عدد الأدوية
            drugs_count = 0
            if pres[5]:
                drugs = json.loads(pres[5])
                drugs_count = len(drugs)
                
            self.prescription_tree.insert('', 'end', values=(
                pres[1], pres[2], pres[3], pres[4],
                drugs_count, pres[6], "عرض/حذف"
            ), iid=pres[0])
            
    def load_expiry_products(self):
        """تحميل الأدوية المنتهية أو القريبة من الانتهاء"""
        self.expiry_tree.delete(*self.expiry_tree.get_children())
        
        today = datetime.now().date()
        expiry_limit = today + timedelta(days=90)
        
        self.cursor.execute("""
            SELECT * FROM products 
            WHERE expiry_date IS NOT NULL 
            AND expiry_date <= ?
            ORDER BY expiry_date
        """, (expiry_limit.strftime('%Y-%m-%d'),))
        
        products = self.cursor.fetchall()
        
        for product in products:
            expiry_date = datetime.strptime(product[10], '%Y-%m-%d').date()
            days_left = (expiry_date - today).days
            
            total_value = product[6] * product[8]
            
            self.expiry_tree.insert('', 'end', values=(
                product[2], product[8], product[10],
                days_left, f"{product[6]:.2f}", f"{total_value:.2f}", "حذف"
            ), iid=product[0])
            
    def update_dashboard(self):
        """تحديث إحصائيات لوحة التحكم"""
        # إجمالي الأدوية
        self.cursor.execute("SELECT COUNT(*) FROM products")
        total_products = self.cursor.fetchone()[0]
        
        # الأدوية المنخفضة المخزون
        self.cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= min_stock")
        low_stock = self.cursor.fetchone()[0]
        
        # فواتير اليوم
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM sales WHERE date = ?", (today,))
        today_sales = self.cursor.fetchone()
        
        # المرضى المسجلين
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = self.cursor.fetchone()[0]
        
        # الأدوية القريبة من الانتهاء
        expiry_limit = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        self.cursor.execute("""
            SELECT COUNT(*) FROM products 
            WHERE expiry_date IS NOT NULL 
            AND expiry_date <= ? 
            AND expiry_date >= ?
        """, (expiry_limit, datetime.now().strftime('%Y-%m-%d')))
        expiring_soon = self.cursor.fetchone()[0]
        
        # تحديث الشجرة في لوحة التحكم
        self.alert_tree.delete(*self.alert_tree.get_children())
        
        # الحصول على التنبيهات
        self.cursor.execute("""
            SELECT name, quantity, min_stock, expiry_date 
            FROM products 
            WHERE quantity <= min_stock 
               OR (expiry_date IS NOT NULL AND expiry_date <= ?)
            ORDER BY expiry_date
        """, (expiry_limit,))
        
        alerts = self.cursor.fetchall()
        
        for alert in alerts:
            expiry_date = alert[3]
            days_left = "غير محدد"
            if expiry_date:
                expiry_date_obj = datetime.strptime(expiry_date, '%Y-%m-%d').date()
                today_obj = datetime.now().date()
                days_left = (expiry_date_obj - today_obj).days
                
            status = "منخفض" if alert[1] <= alert[2] else "قريب الانتهاء"
            
            self.alert_tree.insert('', 'end', values=(
                alert[0], alert[1], alert[2], 
                expiry_date if expiry_date else "غير محدد",
                status
            ))
            
    def add_product_dialog(self):
        """فتح نافذة إضافة دواء جديد"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة دواء جديد")
        dialog.geometry("600x500")
        
        # إنشاء حقول الإدخال
        fields = [
            ("اسم الدواء *", "name", True),
            ("باركود", "barcode", False),
            ("الوحدة", "unit", False),
            ("الشكل الصيدلاني", "type", False),
            ("الشركة المصنعة", "manufacturer", False),
            ("سعر الشراء *", "purchase_price", True),
            ("سعر البيع *", "sale_price", True),
            ("الكمية *", "quantity", True),
            ("الحد الأدنى للمخزون", "min_stock", False),
            ("تاريخ الانتهاء", "expiry_date", False)
        ]
        
        entries = {}
        for i, (label, field, required) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            
            if field == 'expiry_date':
                entry = DateEntry(dialog, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(dialog, width=30)
                
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry
            
            if required:
                ttk.Label(dialog, text="*", foreground="red").grid(row=i, column=2, padx=5)
                
        # أزرار
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="إلغاء", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="حفظ", 
                  command=lambda: self.save_product(entries, dialog)).pack(side=tk.LEFT, padx=10)
            
    def save_product(self, entries, dialog):
        """حفظ المنتج في قاعدة البيانات"""
        try:
            # التحقق من الحقول المطلوبة
            required_fields = ['name', 'purchase_price', 'sale_price', 'quantity']
            for field in required_fields:
                if not entries[field].get().strip():
                    messagebox.showerror("خطأ", f"يرجى ملء حقل {field}")
                    return
                    
            # تجميع البيانات
            data = {
                'barcode': entries['barcode'].get(),
                'name': entries['name'].get(),
                'unit': entries['unit'].get() or 'عبوة',
                'type': entries['type'].get(),
                'manufacturer': entries['manufacturer'].get(),
                'purchase_price': float(entries['purchase_price'].get()),
                'sale_price': float(entries['sale_price'].get()),
                'quantity': int(entries['quantity'].get()),
                'min_stock': int(entries['min_stock'].get() or 10),
                'expiry_date': entries['expiry_date'].get() if hasattr(entries['expiry_date'], 'get') else None
            }
            
            # إدخال في قاعدة البيانات
            self.cursor.execute("""
                INSERT INTO products 
                (barcode, name, unit, type, manufacturer, purchase_price, 
                 sale_price, quantity, min_stock, expiry_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['barcode'], data['name'], data['unit'], data['type'],
                data['manufacturer'], data['purchase_price'], data['sale_price'],
                data['quantity'], data['min_stock'], data['expiry_date']
            ))
            
            self.conn.commit()
            messagebox.showinfo("نجاح", "تم إضافة الدواء بنجاح")
            
            # تحديث البيانات
            self.load_products()
            self.update_dashboard()
            self.load_expiry_products()
            
            dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            
    def on_product_double_click(self, event):
        """معالجة النقر المزدوج على منتج"""
        item = self.product_tree.selection()[0]
        product_id = item
        
        # فتح نافذة التعديل
        self.edit_product_dialog(product_id)
        
    def edit_product_dialog(self, product_id):
        """فتح نافذة تعديل المنتج"""
        # جلب بيانات المنتج من قاعدة البيانات
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = self.cursor.fetchone()
        
        if not product:
            messagebox.showerror("خطأ", "المنتج غير موجود")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("تعديل بيانات الدواء")
        dialog.geometry("600x500")
        
        # إنشاء حقول الإدخال
        fields = [
            ("اسم الدواء *", "name", True, product[2]),
            ("باركود", "barcode", False, product[1]),
            ("الوحدة", "unit", False, product[3]),
            ("الشكل الصيدلاني", "type", False, product[4]),
            ("الشركة المصنعة", "manufacturer", False, product[5]),
            ("سعر الشراء *", "purchase_price", True, product[6]),
            ("سعر البيع *", "sale_price", True, product[7]),
            ("الكمية *", "quantity", True, product[8]),
            ("الحد الأدنى للمخزون", "min_stock", False, product[9]),
            ("تاريخ الانتهاء", "expiry_date", False, product[10])
        ]
        
        entries = {}
        for i, (label, field, required, value) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            
            if field == 'expiry_date':
                entry = DateEntry(dialog, date_pattern='yyyy-mm-dd')
                if value:
                    entry.set_date(datetime.strptime(value, '%Y-%m-%d'))
            else:
                entry = ttk.Entry(dialog, width=30)
                if value is not None:
                    entry.insert(0, str(value))
                    
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry
            
            if required:
                ttk.Label(dialog, text="*", foreground="red").grid(row=i, column=2, padx=5)
                
        # أزرار
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="حذف", 
                  command=lambda: self.delete_product(product_id, dialog)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="إلغاء", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="حفظ التعديلات", 
                  command=lambda: self.update_product(product_id, entries, dialog)).pack(side=tk.LEFT, padx=10)
            
    def update_product(self, product_id, entries, dialog):
        """تحديث بيانات المنتج"""
        try:
            # التحقق من الحقول المطلوبة
            required_fields = ['name', 'purchase_price', 'sale_price', 'quantity']
            for field in required_fields:
                if not entries[field].get().strip():
                    messagebox.showerror("خطأ", f"يرجى ملء حقل {field}")
                    return
                    
            # تجميع البيانات
            data = {
                'barcode': entries['barcode'].get(),
                'name': entries['name'].get(),
                'unit': entries['unit'].get() or 'عبوة',
                'type': entries['type'].get(),
                'manufacturer': entries['manufacturer'].get(),
                'purchase_price': float(entries['purchase_price'].get()),
                'sale_price': float(entries['sale_price'].get()),
                'quantity': int(entries['quantity'].get()),
                'min_stock': int(entries['min_stock'].get() or 10),
                'expiry_date': entries['expiry_date'].get() if hasattr(entries['expiry_date'], 'get') else None
            }
            
            # تحديث في قاعدة البيانات
            self.cursor.execute("""
                UPDATE products 
                SET barcode = ?, name = ?, unit = ?, type = ?, manufacturer = ?,
                    purchase_price = ?, sale_price = ?, quantity = ?, 
                    min_stock = ?, expiry_date = ?
                WHERE id = ?
            """, (
                data['barcode'], data['name'], data['unit'], data['type'],
                data['manufacturer'], data['purchase_price'], data['sale_price'],
                data['quantity'], data['min_stock'], data['expiry_date'],
                product_id
            ))
            
            self.conn.commit()
            messagebox.showinfo("نجاح", "تم تحديث الدواء بنجاح")
            
            # تحديث البيانات
            self.load_products()
            self.update_dashboard()
            self.load_expiry_products()
            
            dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            
    def delete_product(self, product_id, dialog=None):
        """حذف منتج"""
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف هذا الدواء؟"):
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
            
            if dialog:
                dialog.destroy()
                
            self.load_products()
            self.update_dashboard()
            self.load_expiry_products()
            
    def add_customer_dialog(self):
        """فتح نافذة إضافة مريض جديد"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة مريض جديد")
        dialog.geometry("500x400")
        
        # حقول الإدخال
        fields = [
            ("اسم المريض *", "name", True),
            ("العمر", "age", False),
            ("الهاتف", "phone", False),
            ("التشخيص / الأمراض", "diagnosis", False),
            ("آخر زيارة", "last_visit", False)
        ]
        
        entries = {}
        for i, (label, field, required) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            
            if field == 'last_visit':
                entry = DateEntry(dialog, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(dialog, width=30)
                
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry
            
            if required:
                ttk.Label(dialog, text="*", foreground="red").grid(row=i, column=2, padx=5)
                
        # أزرار
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="إلغاء", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="حفظ", 
                  command=lambda: self.save_customer(entries, dialog)).pack(side=tk.LEFT, padx=10)
            
    def save_customer(self, entries, dialog):
        """حفظ المريض في قاعدة البيانات"""
        try:
            if not entries['name'].get().strip():
                messagebox.showerror("خطأ", "يرجى إدخال اسم المريض")
                return
                
            # تجميع البيانات
            data = {
                'name': entries['name'].get(),
                'age': entries['age'].get(),
                'phone': entries['phone'].get(),
                'diagnosis': entries['diagnosis'].get(),
                'last_visit': entries['last_visit'].get() if hasattr(entries['last_visit'], 'get') else None
            }
            
            # إدخال في قاعدة البيانات
            self.cursor.execute("""
                INSERT INTO customers (name, age, phone, diagnosis, last_visit)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data['name'], 
                int(data['age']) if data['age'] else None,
                data['phone'],
                data['diagnosis'],
                data['last_visit']
            ))
            
            self.conn.commit()
            messagebox.showinfo("نجاح", "تم إضافة المريض بنجاح")
            
            # تحديث البيانات
            self.load_customers()
            self.update_dashboard()
            
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            
    def add_supplier_dialog(self):
        """فتح نافذة إضافة مورد جديد"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة مورد جديد")
        dialog.geometry("500x400")
        
        # حقول الإدخال
        fields = [
            ("كود المورد", "code", False),
            ("اسم المورد *", "name", True),
            ("التخصص", "specialty", False),
            ("الهاتف", "phone", False),
            ("البريد الإلكتروني", "email", False),
            ("العنوان", "address", False)
        ]
        
        entries = {}
        for i, (label, field, required) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry
            
            if required:
                ttk.Label(dialog, text="*", foreground="red").grid(row=i, column=2, padx=5)
                
        # أزرار
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="إلغاء", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="حفظ", 
                  command=lambda: self.save_supplier(entries, dialog)).pack(side=tk.LEFT, padx=10)
            
    def save_supplier(self, entries, dialog):
        """حفظ المورد في قاعدة البيانات"""
        try:
            if not entries['name'].get().strip():
                messagebox.showerror("خطأ", "يرجى إدخال اسم المورد")
                return
                
            # تجميع البيانات
            data = {
                'code': entries['code'].get(),
                'name': entries['name'].get(),
                'specialty': entries['specialty'].get(),
                'phone': entries['phone'].get(),
                'email': entries['email'].get(),
                'address': entries['address'].get()
            }
            
            # إدخال في قاعدة البيانات
            self.cursor.execute("""
                INSERT INTO suppliers (code, name, specialty, phone, email, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['code'], data['name'], data['specialty'],
                data['phone'], data['email'], data['address']
            ))
            
            self.conn.commit()
            messagebox.showinfo("نجاح", "تم إضافة المورد بنجاح")
            
            # تحديث البيانات
            self.load_suppliers()
            
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            
    def add_sales_invoice_dialog(self):
        """فتح نافذة إضافة فاتورة صرف جديدة"""
        dialog = tk.Toplevel(self.root)
        dialog.title("فاتورة صرف جديدة")
        dialog.geometry("800x600")
        
        # حقول الفاتورة
        ttk.Label(dialog, text="رقم الفاتورة:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        invoice_number = ttk.Entry(dialog, width=20)
        invoice_number.insert(0, f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        invoice_number.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="التاريخ:").grid(row=0, column=2, padx=10, pady=5, sticky='w')
        invoice_date = DateEntry(dialog, date_pattern='yyyy-mm-dd')
        invoice_date.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(dialog, text="اسم المريض:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        patient_name = ttk.Entry(dialog, width=30)
        patient_name.grid(row=1, column=1, padx=10, pady=5, columnspan=3, sticky='w')
        
        ttk.Label(dialog, text="طريقة الدفع:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        payment_method = ttk.Combobox(dialog, values=["نقدي", "بطاقة ائتمان", "تأمين"])
        payment_method.current(0)
        payment_method.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # إضافة الأدوية
        items_frame = ttk.LabelFrame(dialog, text="الأدوية", padding=10)
        items_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        # شجرة الأدوية
        columns = ("الدواء", "الكمية", "السعر", "الإجمالي")
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=5)
        
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=150)
            
        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=items_tree.yview)
        items_tree.configure(yscrollcommand=scrollbar.set)
        
        items_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # حقل البحث عن دواء
        search_frame = ttk.Frame(dialog)
        search_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky='w')
        
        ttk.Label(search_frame, text="ابحث عن دواء:").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # الإجماليات
        totals_frame = ttk.Frame(dialog)
        totals_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
        
        ttk.Label(totals_frame, text="الإجمالي:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        subtotal_label = ttk.Label(totals_frame, text="0.00 ريال")
        subtotal_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        ttk.Label(totals_frame, text="الضريبة (15%):").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tax_label = ttk.Label(totals_frame, text="0.00 ريال")
        tax_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        ttk.Label(totals_frame, text="المبلغ الإجمالي:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        total_label = ttk.Label(totals_frame, text="0.00 ريال", font=('Arial', 12, 'bold'))
        total_label.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # أزرار
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=6, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="إلغاء", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="حفظ الفاتورة", 
                  command=lambda: self.save_sales_invoice(
                      invoice_number, invoice_date, patient_name, 
                      payment_method, items_tree, dialog)).pack(side=tk.LEFT, padx=10)
            
    def save_sales_invoice(self, invoice_number, invoice_date, patient_name, 
                          payment_method, items_tree, dialog):
        """حفظ الفاتورة في قاعدة البيانات"""
        try:
            # جمع عناصر الفاتورة
            items = []
            for item in items_tree.get_children():
                values = items_tree.item(item)['values']
                items.append({
                    'name': values[0],
                    'quantity': values[1],
                    'price': values[2],
                    'total': values[3]
                })
                
            if not items:
                messagebox.showerror("خطأ", "يجب إضافة أدوية على الأقل للفاتورة")
                return
                
            # حساب الإجماليات
            subtotal = sum(float(item['total']) for item in items)
            tax = subtotal * 0.15
            total_amount = subtotal + tax
            
            # إدخال في قاعدة البيانات
            self.cursor.execute("""
                INSERT INTO sales (invoice_number, date, patient_name, 
                                 total_amount, payment_method, items)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                invoice_number.get(),
                invoice_date.get(),
                patient_name.get(),
                total_amount,
                payment_method.get(),
                json.dumps(items, ensure_ascii=False)
            ))
            
            self.conn.commit()
            messagebox.showinfo("نجاح", "تم حفظ الفاتورة بنجاح")
            
            # تحديث البيانات
            self.load_sales()
            self.update_dashboard()
            
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            
    def add_prescription_dialog(self):
        """فتح نافذة إضافة وصفة طبية جديدة"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة وصفة طبية جديدة")
        dialog.geometry("700x600")
        
        # حقول الوصفة
        ttk.Label(dialog, text="رقم الوصفة:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        prescription_number = ttk.Entry(dialog, width=20)
        prescription_number.insert(0, f"RX-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        prescription_number.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="التاريخ:").grid(row=0, column=2, padx=10, pady=5, sticky='w')
        prescription_date = DateEntry(dialog, date_pattern='yyyy-mm-dd')
        prescription_date.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(dialog, text="اسم المريض:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        patient_name = ttk.Entry(dialog, width=30)
        patient_name.grid(row=1, column=1, padx=10, pady=5, columnspan=3, sticky='w')
        
        ttk.Label(dialog, text="اسم الطبيب:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        doctor_name = ttk.Entry(dialog, width=30)
        doctor_name.grid(row=2, column=1, padx=10, pady=5, columnspan=3, sticky='w')
        
        ttk.Label(dialog, text="حالة الوصفة:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        status = ttk.Combobox(dialog, values=["معلقة", "مكتملة", "ملغاة"])
        status.current(0)
        status.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        
        # ملاحظات
        ttk.Label(dialog, text="ملاحظات:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        notes_text = tk.Text(dialog, height=5, width=50)
        notes_text.grid(row=4, column=1, columnspan=3, padx=10, pady=5)
        
        # أزرار
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="إلغاء", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="حفظ الوصفة", 
                  command=lambda: self.save_prescription(
                      prescription_number, prescription_date, patient_name,
                      doctor_name, status, notes_text, dialog)).pack(side=tk.LEFT, padx=10)
            
    def save_prescription(self, prescription_number, prescription_date, patient_name,
                         doctor_name, status, notes_text, dialog):
        """حفظ الوصفة في قاعدة البيانات"""
        try:
            if not prescription_number.get().strip():
                messagebox.showerror("خطأ", "يرجى إدخال رقم الوصفة")
                return
                
            if not patient_name.get().strip():
                messagebox.showerror("خطأ", "يرجى إدخال اسم المريض")
                return
                
            if not doctor_name.get().strip():
                messagebox.showerror("خطأ", "يرجى إدخال اسم الطبيب")
                return
                
            # إدخال في قاعدة البيانات
            self.cursor.execute("""
                INSERT INTO prescriptions 
                (prescription_number, date, patient_name, doctor_name, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                prescription_number.get(),
                prescription_date.get(),
                patient_name.get(),
                doctor_name.get(),
                status.get(),
                notes_text.get("1.0", tk.END).strip()
            ))
            
            self.conn.commit()
            messagebox.showinfo("نجاح", "تم حفظ الوصفة بنجاح")
            
            # تحديث البيانات
            self.load_prescriptions()
            
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            
    def generate_report(self):
        """توليد التقرير"""
        report_type = self.report_type.get()
        from_date = self.report_from_date.get()
        to_date = self.report_to_date.get()
        
        # مسح الشجرة الحالية
        self.report_tree.delete(*self.report_tree.get_children())
        
        if report_type == "تقرير المبيعات":
            self.generate_sales_report(from_date, to_date)
        elif report_type == "تقرير المخزون":
            self.generate_inventory_report()
        elif report_type == "تقرير الأدوية المنتهية":
            self.generate_expiry_report()
        elif report_type == "تقرير المرضى":
            self.generate_customers_report()
        elif report_type == "تقرير الوصفات الطبية":
            self.generate_prescriptions_report(from_date, to_date)
            
    def generate_sales_report(self, from_date, to_date):
        """توليد تقرير المبيعات"""
        self.cursor.execute("""
            SELECT * FROM sales 
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        """, (from_date, to_date))
        
        sales = self.cursor.fetchall()
        total_amount = 0
        
        for sale in sales:
            items = json.loads(sale[6]) if sale[6] else []
            items_count = len(items)
            
            self.report_tree.insert('', 'end', values=(
                sale[2], f"فاتورة {sale[1]}", items_count,
                f"{sale[4]:.2f} ريال", f"{sale[4]:.2f} ريال"
            ))
            
            total_amount += sale[4]
            
        # إضافة صف الإجمالي
        if sales:
            self.report_tree.insert('', 'end', values=(
                "", "<strong>الإجمالي</strong>", "", 
                "", f"<strong>{total_amount:.2f} ريال</strong>"
            ))
            
    def generate_inventory_report(self):
        """توليد تقرير المخزون"""
        self.cursor.execute("SELECT * FROM products ORDER BY name")
        products = self.cursor.fetchall()
        total_value = 0
        
        for product in products:
            product_value = product[6] * product[8]
            total_value += product_value
            
            self.report_tree.insert('', 'end', values=(
                datetime.now().strftime('%Y-%m-%d'), product[2], product[8],
                f"{product[6]:.2f} ريال", f"{product_value:.2f} ريال"
            ))
            
        # إضافة صف الإجمالي
        if products:
            self.report_tree.insert('', 'end', values=(
                "", "<strong>إجمالي قيمة المخزون</strong>", "", 
                "", f"<strong>{total_value:.2f} ريال</strong>"
            ))
            
    def generate_expiry_report(self):
        """توليد تقرير الأدوية المنتهية"""
        today = datetime.now().date()
        
        self.cursor.execute("""
            SELECT * FROM products 
            WHERE expiry_date IS NOT NULL 
            ORDER BY expiry_date
        """)
        
        products = self.cursor.fetchall()
        total_value = 0
        
        for product in products:
            expiry_date = datetime.strptime(product[10], '%Y-%m-%d').date()
            days_left = (expiry_date - today).days
            product_value = product[6] * product[8]
            total_value += product_value
            
            status = "منتهي" if days_left < 0 else "قريب الانتهاء"
            
            self.report_tree.insert('', 'end', values=(
                product[10], product[2], product[8],
                f"{product[6]:.2f} ريال", f"{product_value:.2f} ريال"
            ))
            
    def generate_customers_report(self):
        """توليد تقرير المرضى"""
        self.cursor.execute("SELECT * FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        
        for customer in customers:
            self.report_tree.insert('', 'end', values=(
                customer[5] if customer[5] else "لم يزر بعد",
                customer[1], customer[2] if customer[2] else "غير محدد",
                customer[3] if customer[3] else "غير محدد",
                customer[4] if customer[4] else "غير محدد"
            ))
            
    def generate_prescriptions_report(self, from_date, to_date):
        """توليد تقرير الوصفات الطبية"""
        self.cursor.execute("""
            SELECT * FROM prescriptions 
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        """, (from_date, to_date))
        
        prescriptions = self.cursor.fetchall()
        
        for pres in prescriptions:
            drugs = json.loads(pres[5]) if pres[5] else []
            drugs_count = len(drugs)
            
            self.report_tree.insert('', 'end', values=(
                pres[2], pres[3], pres[4], drugs_count, pres[6]
            ))
            
    def import_from_excel(self):
        """استيراد البيانات من ملف CSV (محاكاة لـ Excel)"""
        file_path = filedialog.askopenfilename(
            title="اختر ملف CSV للاستيراد",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                imported_count = 0
                
                for row in reader:
                    # تحويل البيانات
                    try:
                        self.cursor.execute("""
                            INSERT INTO products 
                            (barcode, name, unit, type, manufacturer, purchase_price, 
                             sale_price, quantity, min_stock, expiry_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row.get('الباركود', ''),
                            row.get('اسم الدواء', 'غير محدد'),
                            row.get('الوحدة', 'عبوة'),
                            row.get('الشكل الصيدلاني', ''),
                            row.get('الشركة المصنعة', ''),
                            float(row.get('سعر الشراء', 0)),
                            float(row.get('سعر البيع', 0)),
                            int(row.get('الكمية', 0)),
                            int(row.get('الحد الأدنى للمخزون', 10)),
                            row.get('تاريخ الانتهاء', None)
                        ))
                        
                        imported_count += 1
                    except Exception as e:
                        print(f"خطأ في استيراد سطر: {e}")
                        
                self.conn.commit()
                messagebox.showinfo("نجاح", f"تم استيراد {imported_count} منتج بنجاح")
                
                # تحديث البيانات
                self.load_products()
                self.update_dashboard()
                self.load_expiry_products()
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في الاستيراد: {str(e)}")
            
    def export_to_excel(self):
        """تصدير البيانات إلى ملف CSV (محاكاة لـ Excel)"""
        file_path = filedialog.asksaveasfilename(
            title="حفظ الملف",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            # جلب جميع المنتجات
            self.cursor.execute("SELECT * FROM products")
            products = self.cursor.fetchall()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # كتابة العناوين
                headers = ["الباركود", "اسم الدواء", "الوحدة", "الشكل الصيدلاني", 
                          "الشركة المصنعة", "سعر الشراء", "سعر البيع", 
                          "الكمية", "الحد الأدنى للمخزون", "تاريخ الانتهاء"]
                writer.writerow(headers)
                
                # كتابة البيانات
                for product in products:
                    writer.writerow([
                        product[1], product[2], product[3], product[4], product[5],
                        product[6], product[7], product[8], product[9], product[10]
                    ])
                    
            messagebox.showinfo("نجاح", f"تم التصدير إلى {file_path}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في التصدير: {str(e)}")
            
    def delete_all_products(self):
        """حذف جميع المنتجات"""
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف جميع المنتجات؟"):
            self.cursor.execute("DELETE FROM products")
            self.conn.commit()
            
            self.load_products()
            self.update_dashboard()
            self.load_expiry_products()
            
            messagebox.showinfo("نجاح", "تم حذف جميع المنتجات")

def main():
    root = tk.Tk()
    app = PharmacyInventorySystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()