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

android.minapi = 24
android.archs = arm64-v8a

android.accept_sdk_license = True
android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 0
