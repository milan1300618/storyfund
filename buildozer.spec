# StoryFund - stable python-for-android configuration

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
android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True
android.skip_update = False
android.allow_backup = True

#
# IMPORTANT:
# This p4a commit is immediately before the Python 3.14 update.
# It uses Python 3.11.13 for the Android Python recipe.
#

p4a.branch = develop
p4a.commit = 7593f9d

[buildozer]

log_level = 2
warn_on_root = 1
