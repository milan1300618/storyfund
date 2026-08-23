# Buildozer configuration for StoryFund

[app]

title = StoryFund
package.name = storyfund
package.domain = org.storyfund

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 24
android.ndk = 27c
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

osx.kivy_version = 2.2.0

[buildozer]

log_level = 2
warn_on_root = 1
