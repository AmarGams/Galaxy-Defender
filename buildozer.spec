[app]

title = Galaxy Defender
package.name = galaxydefender
package.domain = org.amargams

source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,mp3,wav,ogg,txt
source.exclude_dirs = tests, bin, .github, .git, .buildozer
source.exclude_patterns = Galaxy-Defender-Pydroid3.zip,*.yml,*.yaml,*.md,*.zip

version = 1.0

# This version combo is the one that most often works for Pygame Android builds.
requirements = python3==3.10.12,hostpython3==3.10.12,kivy==2.3.0,pyjnius==1.5.0,pygame

orientation = landscape
fullscreen = 1

android.permissions = INTERNET,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
