[app]

title = StoryFund
package.name = myapp
package.domain = storyfund

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,txt

version = 0.1
android.numeric_version = 10242

requirements = python3,kivy==2.2.1,kivymd==1.2.0,requests,certifi,pay-by-square,segno,liblzma

orientation = portrait
fullscreen = 0

android.api = 36
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.accept_sdk_license = True
android.release_artifact = aab

p4a.branch = v2023.09.16

[buildozer]

log_level = 2
warn_on_root = 0
