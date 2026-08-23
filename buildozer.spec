# StoryFund - Buildozer configuration

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

android.accept_sdk_license = True
android.skip_update = False
android.allow_backup = True

#
# python-for-android:
# 869c74b contains the upstream fix for the
# "Backend 'setuptools.build_meta' is not available" error
# caused by the host-python PYTHONPATH handling.
# It predates the later p4a Python 3.14 changes.
#

p4a.branch = develop
p4a.commit = 869c74b

[buildozer]

log_level = 2
warn_on_root = 1
