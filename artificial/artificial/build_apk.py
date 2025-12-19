# artificial/build_apk.py
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # جذر المستودع
ART = ROOT / "artificial"
SRC = ART / "app_src"
SPEC = ART / "buildozer.spec"
DIST = ART / "dist"

def ensure_structure():
    DIST.mkdir(parents=True, exist_ok=True)
    if not SRC.exists():
        raise FileNotFoundError("لم يتم العثور على artificial/app_src. أنشئه وضع فيه main.py.")

    if not SPEC.exists():
        raise FileNotFoundError("لم يتم العثور على artificial/buildozer.spec. أنشئه كما في المثال.")

def run_buildozer():
    # ننفّذ buildozer داخل مجلد artificial ليأخذ spec الصحيح
    cmd = ["buildozer", "-v", "android", "debug"]
    subprocess.run(cmd, cwd=ART, check=True)

def copy_apk_to_dist():
    # مسار الـ bin الافتراضي الذي يضع فيه buildozer الـ APK
    bin_dir = ART / "bin"
    if not bin_dir.exists():
        raise FileNotFoundError("لم يتم العثور على مجلد bin بعد البناء.")
    apks = list(bin_dir.glob("*.apk"))
    if not apks:
        raise FileNotFoundError("لا يوجد ملفات APK في bin. تحقق من سجل البناء.")
    latest = max(apks, key=lambda p: p.stat().st_mtime)
    target = DIST / latest.name
    shutil.copy2(latest, target)
    print(f"تم نسخ الـ APK إلى: {target}")

def main():
    ensure_structure()
    print("بدء البناء... قد يستغرق وقتًا أول مرة.")
    run_buildozer()
    copy_apk_to_dist()
    print("اكتمل البناء ✅")

if __name__ == "__main__":
    main()