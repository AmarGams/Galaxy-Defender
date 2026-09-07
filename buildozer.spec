[app]

title = Galaxy Defender
package.name = galaxydefender
package.domain = org.amargams

source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,mp3,wav,ogg,txt
source.exclude_dirs = tests, bin, .github, .git, .buildozer
source.exclude_patterns = Galaxy-Defender-Pydroid3.zip,*.yml,*.yaml,*.md,*.zip

version = 1.0

# Do not pin old pyjnius; 1.5.0 breaks with modern setuptools (PYX_FILES error).
requirements = python3,pygame,sdl2,pyjnius
orientation = landscape
fullscreen = 1

android.permissions = INTERNET,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a

# Newer recipes fix pyjnius / pygame Android builds.
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 0
