[app]

title = StoryFund
package.name = storyfund
package.domain = org.storyfund

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,txt

version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Build only the 64-bit Android architecture to keep the APK smaller.
android.archs = arm64-v8a

android.accept_sdk_license = True
android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 1
