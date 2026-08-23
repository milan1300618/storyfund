import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from backend import block_user, unblock_user

Builder.load_file(os.path.join(os.path.dirname(__file__), "user_detail.kv"))


class UserDetailScreen(MDScreen):

    current_user = None

    def show_user(self, user):
        self.current_user = user

        self.ids.nik_label.text = f"NIK: {user.get('nik', '')}"
        self.ids.pin_label.text = f"PIN: {user.get('pin', '')}"

        status = "AKTÍVNY" if user.get("active", True) else "BLOKOVANÝ"
        self.ids.status_label.text = f"Stav: {status}"

        self.ids.stories_label.text = (
    f"Príbehy v kole: {user.get('stories_count', 0)}"
)

    def back(self):
        self.manager.current = "users"

    def block_user(self):
        if self.current_user:
            block_user(self.current_user["nik"])
            self.current_user["active"] = False
            self.ids.status_label.text = "Stav: BLOKOVANÝ"

    def unblock_user(self):
        if self.current_user:
            unblock_user(self.current_user["nik"])
            self.current_user["active"] = True
            self.ids.status_label.text = "Stav: AKTÍVNY"
