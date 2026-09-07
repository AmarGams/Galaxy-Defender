[app]

title = Galaxy Defender
package.name = galaxydefender
package.domain = org.amargams

source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,mp3,wav,ogg,txt
source.exclude_dirs = tests, bin, .github, .git, .buildozer
source.exclude_patterns = Galaxy-Defender-Pydroid3.zip,*.yml,*.yaml,*.md,*.zip

version = 1.0

# p4a develop pulled Python 3.14, which breaks pygame (longintrepr.h).
# Master + Python 3.11 is the combo pygame recipes expect.
requirements = python3==3.11.10,hostpython3==3.11.10,pygame,sdl2
orientation = landscape
fullscreen = 1

android.permissions = INTERNET,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
