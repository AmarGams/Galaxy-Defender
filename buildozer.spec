[app]

title = Galaxy Defender
package.name = galaxydefender
package.domain = org.amargams

source.dir = kivy_app
source.include_exts = py,png,jpg,jpeg,gif,mp3,wav,ogg,txt
icon.filename = %(source.dir)s/icon.png

source.exclude_dirs = tests, bin, .github, .git, .buildozer
source.exclude_patterns = Galaxy-Defender-Pydroid3.zip,*.yml,*.yaml,*.md,*.zip,*.ipynb

version = 1.0

requirements = python3,kivy

orientation = landscape
fullscreen = 1

android.permissions = INTERNET,VIBRATE

android.api = 33
android.minapi = 24
android.accept_sdk_license = True
android.archs = arm64-v8a

p4a.branch = v2024.01.21
p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 0
