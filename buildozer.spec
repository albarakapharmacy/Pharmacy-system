[app]
title = PharmacyApp
package.name = pharmacyapp
package.domain = org.albarakapharmacy
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 1.0
main.py = main.py

requirements = python3,kivy
orientation = portrait
android.minapi = 21
android.sdk = 33
include_exts = py,kv,png,jpg,db

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# بضبط هذه القيم يتعرف Buildozer على ملفات الواجهة والشاشات
# تأكد أن جميع الشاشات لها ملف py ووجود pharmacy.kv في المشروع

[buildozer]
log_level = 2
warn_on_root = 1