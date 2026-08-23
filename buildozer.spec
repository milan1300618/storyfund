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
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.skip_update = False
android.allow_backup = True

#
# Pin python-for-android to the last commit BEFORE the
# Python 3.14 change. This avoids the current p4a 3.14/pip
# BuildDependencyInstallError seen in the build log.
#

p4a.branch = develop
p4a.commit = c02cf78

[buildozer]

log_level = 2
warn_on_root = 1
