[app]
# (str) عنوان التطبيق
title = Pharmacy Al-Baraka

# (str) اسم الحزمة (Package name)
package.name = albaraka_pharmacy

# (str) اسم النطاق للحزمة
package.domain = org.sultan

# (str) مسار الكود المصدري
source.dir = .

# (list) الامتدادات المضمنة
source.include_exts = py,png,jpg,db,csv,kv

# (str) إصدار التطبيق
version = 1.0

# (list) المتطلبات - تم إزالة Tkinter وإضافة Kivy
# ملاحظة: sqlite3 مدمجة في بايثون أندرويد لذا نكتفي بذكر python3 و kivy
requirements = python3,kivy

# (str) الملف الرئيسي
source.filename = main.py

# (list) الأذونات - أندرويد 11+ يتطلب أذونات خاصة للذاكرة
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) مستوى الـ API المستهدف
android.api = 33

# (int) الحد الأدنى للـ API
android.minapi = 21

# (str) اتجاه الشاشة 
orientation = landscape

# (bool) ملء الشاشة
fullscreen = 0

# (list) معمارية المعالج
android.archs = arm64-v8a, armeabi-v7a

# (bool) السماح بالنسخ الاحتياطي
android.allow_backup = True

# (list) المجلدات المضمنة (مثل مجلد قاعدة البيانات)
# source.include_dirs = db
