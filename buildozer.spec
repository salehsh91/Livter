[app]

title = Livter
package.name = livter
package.domain = org.livter
source.dir = .
source.include_exts = py,png,jpg,jpeg,wav,ogg,ttf,json,txt
version = 0.1

# opensimplex is NOT listed on purpose: the repo now contains its own
# pure-Python opensimplex.py (no numpy needed).
requirements = python3==3.11.9,hostpython3==3.11.9,pygame

orientation = landscape
fullscreen = 0

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
