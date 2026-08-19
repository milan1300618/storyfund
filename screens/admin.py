from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout

from backend import list_users, create_user
from cycle import force_new_cycle, record_previous_cycle

Builder.load_file("kv/admin.kv")


class AdminScreen(MDScreen):

    def logout(self):
        self.manager.current = "login"

    def show_users(self):
        self.manager.current = "users"

    def create_user(self):
        self.manager.current = "new_user"

    def settings(self):
        self.manager.current = "settings"

    def close_cycle(self):
        try:
            force_new_cycle()
            message = "Kolo bolo úspešne uzavreté a otvorilo sa nové kolo."
        except Exception as e:
            message = str(e)

        MDDialog(title="Uzavrieť kolo", text=message).open()

    def previous_cycle(self):
        amount_field = MDTextField(
            hint_text="Vyzbieraná suma (€)",
            input_filter="float",
            mode="rectangle"
        )
        recipients_field = MDTextField(
            hint_text="Počet príjemcov",
            input_filter="int",
            mode="rectangle"
        )

        content = BoxLayout(
            orientation="vertical",
            spacing="12dp",
            padding="10dp",
            size_hint_y=None,
            height="130dp"
        )
        content.add_widget(amount_field)
        content.add_widget(recipients_field)

        dialog = MDDialog(
            title="Minulé kolo",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ZRUŠIŤ",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDFlatButton(
                    text="ULOŽIŤ",
                    on_release=lambda x: self._save_previous_cycle(
                        amount_field.text, recipients_field.text, dialog
                    )
                ),
            ],
        )
        dialog.open()

    def _save_previous_cycle(self, amount_text, recipients_text, dialog):
        try:
            if not amount_text.strip() or not recipients_text.strip():
                raise ValueError("Vyplň sumu aj počet príjemcov.")

            per_person = record_previous_cycle(
                amount_text.replace(",", "."), recipients_text
            )
            dialog.dismiss()

            MDDialog(
                title="Minulé kolo uložené",
                text=(
                    f"Vyzbierané: {float(amount_text.replace(',', '.')):.2f} €\n"
                    f"Príjemcov: {int(recipients_text)}\n"
                    f"Na jedného: {per_person:.2f} €"
                )
            ).open()

        except Exception as e:
            MDDialog(title="Chyba", text=str(e)).open()

    def history(self):
        self.manager.current = "history"
