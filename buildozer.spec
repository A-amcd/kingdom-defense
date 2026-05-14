[app]

title = Kingdom Defense
package.name = kingdomdefense
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1.0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.ndk = 25b
android.sdk = 24
android.minapi = 21

requirements = python3,pygame

android.build_type = debug

android.orientation = landscape
android.fullscreen = 0

android.icon = %(source.dir)s/icon.png
android.adaptive_icon = %(source.dir)s/icon.png

android.add_assets = .

p4a.source_dir = 
p4a.local_recipes = 
p4a.bootstrap = sdl2
p4a.ndk_api = 21
p4a.sdk = 24

p4a.requirement = pygame
p4a.setup_py = setup.py

[buildozer]
log_level = 2
warn_on_root = 1