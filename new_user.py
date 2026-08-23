import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from backend import generate_nik, generate_pin, create_user

Builder.load_file(os.path.join(os.path.dirname(__file__), "new_user.kv"))


class NewUserScreen(MDScreen):

    def on_pre_enter(self):
        self.generate_new()

    def generate_new(self):
        self.nik = generate_nik()
        self.pin = generate_pin()
        self.ids.nik_label.text = self.nik
        self.ids.pin_label.text = self.pin

    def save_user(self):
        create_user(self.nik, self.pin)
        self.manager.current = "admin"

    def cancel(self):
        self.manager.current = "admin"
