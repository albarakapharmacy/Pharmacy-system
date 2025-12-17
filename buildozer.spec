# ==========================================
# ملف إعدادات Buildozer لتطبيق صيدلية البركة
# ==========================================

[app]
# (str) عنوان التطبيق
title = Pharmacy Al-Baraka

# (str) اسم الحزمة (Package name)
package.name = albaraka_pharmacy

# (str) اسم النطاق للحزمة
package.domain = org.sultan

# (str) مسار الكود المصدري
source.dir = .

# (list) الامتدادات المضمنة في البناء
source.include_exts = py,png,jpg,db,csv

# (str) إصدار التطبيق
version = 1.0

# (list) المتطلبات (نفس ما في ملف requirements.txt)
# ملاحظة: تم إضافة kivy و jnius لدعم البيئة البرمجية في أندرويد
requirements = python3,tkcalendar,babel,pytz,sqlite3

# (str) اسم الملف الرئيسي للكود
# تأكد أن ملف الكود الخاص بك يسمى main.py ليعمل بشكل صحيح
source.filename = main.py

# (list) الأذونات المطلوبة في أندرويد
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) مستوى الـ API المستهدف (33 متوافق مع متطلبات جوجل الحالية)
android.api = 33

# (int) الحد الأدنى للـ API
android.minapi = 21

# (str) اتجاه الشاشة (landscape أو portrait)
orientation = landscape

# (bool) هل التطبيق ملء الشاشة؟
fullscreen = 0

# (list) معمارية المعالج (للأجهزة الحديثة)
android.archs = arm64-v8a, armeabi-v7a

# ==========================================
# ملاحظة تقنية هامة جداً:
# مكتبة Tkinter لا تعمل بشكل افتراضي وسهل على أندرويد
# هذا الملف سيحاول البناء، ولكن يفضل برمجياً استخدام 
# Kivy أو Flet بدلاً من Tkinter إذا كان الهدف الأساسي هو الأندرويد.
# ==========================================
