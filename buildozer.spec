[app]

title = Galaxy Defender
package.name = galaxydefender
package.domain = org.amargams

source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,mp3,wav,ogg,txt
source.exclude_dirs = tests, bin, .github, .git, .buildozer
source.exclude_patterns = Galaxy-Defender-Pydroid3.zip,*.yml,*.yaml,*.md,*.zip,*.ipynb

version = 1.0

# Pygame-only. Do not add kivy (it doubles compile time and often breaks).
# Pin Python 3.11 so p4a does not pick 3.12/3.14 (longintrepr.h).
requirements = python3==3.11.10,hostpython3==3.11.10,pygame
orientation = landscape
fullscreen = 1

android.permissions = INTERNET,VIBRATE
android.api = 33
android.minapi = 24
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 0
