# StoryFund - deliberately pinned to the stable 2022 toolchain

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

# Stable p4a v2022.12.20 toolchain:
# target API 33, minimum API 21, NDK r25b.
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True
android.allow_backup = True

[app:source.exclude_dirs]
__pycache__
.git
.github
.buildozer
bin

#
# Pin python-for-android to the released 2022.12.20 commit.
#
p4a.branch = master
p4a.commit = cc6481b

[buildozer]

log_level = 2
warn_on_root = 1
