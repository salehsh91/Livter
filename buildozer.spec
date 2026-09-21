[app]

title = Livter
package.name = livter
package.domain = org.livter
source.dir = .
source.include_exts = py,png,jpg,jpeg,wav,ogg,ttf,json,txt
version = 0.1

# Python 3.10.12 on purpose: pygame fails to compile with Python 3.11+
# ("longintrepr.h file not found").
# opensimplex is NOT listed on purpose: the repo now contains its own
# pure-Python opensimplex.py (no numpy needed).
requirements = python3==3.10.12,hostpython3==3.10.12,pygame

orientation = landscape
fullscreen = 1

android.accept_sdk_license = True

# Oldest Android that Python 3 + SDL2 can run on is 5.0 (API 21).
android.minapi = 21
android.ndk_api = 21

# Both CPU types: 32-bit phones (many Android 5-8 devices) AND 64-bit phones.
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1
