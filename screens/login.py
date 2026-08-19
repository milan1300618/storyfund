# ======================================
# StoryFund v0.6
# screens/login.py
# ======================================

from config import APP_NAME, APP_VERSION
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from backend import login_user
from firebase_auth import login_admin, login_user_auth

Builder.load_file("kv/login.kv")

current_user = None

ADMIN_EMAIL = "storyfundreg@gmail.com"


class LoginScreen(MDScreen):

    def on_kv_post(self, base_widget):
        # Sledujeme písanie do poľa NIK.
        # Po zadaní prvých 4 znakov "stor" doplníme admin Gmail.
        self.ids.nik.bind(text=self.auto_complete_admin)

    def auto_complete_admin(self, instance, value):
        value = value.strip()

        # Keď používateľ začne písať "stor", doplníme celý admin e-mail.
        if value.lower() == "stor":
            instance.text = ADMIN_EMAIL
            instance.cursor = (len(ADMIN_EMAIL), 0)

    def login(self):
        global current_user

        nik = self.ids.nik.text.strip()
        pin = self.ids.pin.text.strip()

        # ADMIN – Firebase Authentication
        if nik.lower() == ADMIN_EMAIL.lower():
            if login_admin(nik, pin):
                current_user = "ADMIN"
                self.manager.current = "admin"
                return

            self.ids.info.text = "Nesprávny e-mail alebo heslo"
            return

        # BEŽNÝ POUŽÍVATEĽ – NIK + PIN
        # Najprv Firebase Authentication.
        # Používateľ stále zadáva iba NIK + PIN.
        auth_result = login_user_auth(nik, pin)

        if not auth_result.get("ok"):
            self.ids.info.text = "Nesprávny NIK alebo PIN"
            return

        # Až po úspešnom Firebase prihlásení skontrolujeme
        # používateľa v našom users systéme (napr. active/blokovanie).
        if not login_user(nik, pin):
            self.ids.info.text = "Používateľ nie je aktívny"
            return

        current_user = nik
        self.manager.current = "home"
        return


def get_current_user():
    return current_user
