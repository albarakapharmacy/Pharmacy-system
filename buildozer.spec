[app]
title = PharmacyApp
package.name = pharmacyapp
package.domain = org.albarakapharmacy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0
main.py = main.py

requirements = python3,kivy,sqlite3

orientation = portrait
android.minapi = 21
android.sdk = 33
include_exts = py,kv,png,jpg,db
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

[buildozer]
log_level = 2
warn_on_root = 1