[app]

title = StoryFund
package.name = storyfund
package.domain = org.storyfund

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,txt

version = 0.1

requirements = python3,kivy==2.2.0,kivymd==1.2.0,requests

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 0
