[app]
title = PharmacyApp
package.name = pharmacyapp
package.domain = org.albarakapharmacy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0

# اسم ملف Python الرئيسي
main.py = main.py

requirements = python3,kivy,sqlite3

orientation = portrait

# أيقونة (اختياري) ضع مسار أيقونتك هنا
# icon.filename = %(source.dir)s/icon.png

# الحد الأدنى لإصدار Android (21 = Android 5.0)
android.minapi = 21

# الإصدار المستهدف
android.sdk = 33

# دعم التوجيه العربي
android.extra_args = --resource-config-ar

# لمنع إطفاء الشاشة أثناء العمل
android.presplash_color = #1976D2

# حفظ بيانات التطبيق (يضع db تلقائيا في مجلد app)
android.permission = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# دعم ضغط ملف apk
android.debug = 1

# تضمين جميع ملفات kv والصور الافتراضية
include_exts = py,kv,png,jpg,db

# لمنع التضييق على الأذونات
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# دعم للتخزين الداخلي
# (جرب التطبيق دون هذا السطر غالبًا يعمل تلقائياً مع كودك)

# لغة برمجة الجافا سكريبت إن كنت بحاجة اليها لاحقاً
# android.add_javac_classes = org/example/myclass.java

# ----------------------
# لا تعدل هذه الأسطر بدون معرفة
# ----------------------
[buildozer]
log_level = 2
warn_on_root = 1