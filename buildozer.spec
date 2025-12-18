[app]
title = Pharmacy Al-Baraka
package.name = pharmacy
package.domain = org.albaraka

source.dir = .
source.include_exts = py,kv,png,jpg,db,ttf,csv

version = 1.0

requirements = python3,kivy,sqlite3,pyzbar,pillow,plyer

orientation = landscape
fullscreen = 0

android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

log_level = 2