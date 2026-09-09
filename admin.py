import os

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.clipboard import Clipboard

from backend import list_users, create_user
from cycle import force_new_cycle, record_previous_cycle
from database import get_archive

Builder.load_file(
    os.path.join(os.path.dirname(__file__), "admin.kv")
)


class AdminScreen(MDScreen):

    def logout(self):
        self.manager.current = "login"

    def show_users(self):
        self.manager.current = "users"

    def create_user(self):
        self.manager.current = "new_user"

    def settings(self):
        self.manager.current = "settings"

    def _show_message(self, title, text):
        ok_button = MDButton(
            MDButtonText(text="OK"),
            style="text"
        )

        dialog = MDDialog(
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=text),
            MDDialogButtonContainer(
                Widget(),
                ok_button,
            ),
        )

        ok_button.bind(
            on_release=lambda *args: dialog.dismiss()
        )

        dialog.open()

    # =====================================
    # UZAVRETIE KOLA
    # =====================================

    def close_cycle(self):

        try:

            force_new_cycle()

            archive = get_archive()

            winners = []

            if archive:

                last = archive[-1]

                winners = last.get(
                    "winners",
                    []
                )

            if not isinstance(winners, list):
                winners = []

            winners = [
                str(w).strip()
                for w in winners
                if str(w).strip()
            ]

            if winners:

                self.show_winners(winners)

            else:

                self._show_message(
                    "Kolo uzavreté",
                    (
                        "Kolo bolo úspešne uzavreté "
                        "a otvorilo sa nové kolo.\n\n"
                        "V tomto kole neboli vyžrebovaní "
                        "žiadni výhercovia."
                    )
                )

        except Exception as e:

            self._show_message(
                "Chyba pri uzatváraní kola",
                str(e)
            )

    # =====================================
    # ZOBRAZENIE VÝHERCOV
    # =====================================

    def show_winners(self, winners):

        winners_text = "\n".join(winners)

        winners_field = TextInput(
            text=winners_text,
            multiline=True,
            readonly=True,
            font_size="18sp",
            size_hint_y=None,
            height="300dp",
            padding=("12dp", "12dp")
        )

        content = BoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="10dp",
            size_hint_y=None,
            height="370dp"
        )

        content.add_widget(winners_field)

        copy_button = MDButton(
            MDButtonText(text="KOPÍROVAŤ ZOZNAM"),
            style="text"
        )

        close_button = MDButton(
            MDButtonText(text="ZAVRIEŤ"),
            style="text"
        )

        dialog = MDDialog(
            MDDialogHeadlineText(
                text=f"VÝHERCI ({len(winners)})"
            ),
            MDDialogContentContainer(
                content,
                orientation="vertical"
            ),
            MDDialogButtonContainer(
                Widget(),
                copy_button,
                close_button,
                spacing="8dp"
            ),
        )

        copy_button.bind(
            on_release=lambda *args: self.copy_winners(
                winners_text,
                dialog
            )
        )

        close_button.bind(
            on_release=lambda *args: dialog.dismiss()
        )

        dialog.open()

    # =====================================
    # KOPÍROVANIE VÝHERCOV
    # =====================================

    def copy_winners(self, winners_text, dialog):

        Clipboard.copy(winners_text)

        dialog.dismiss()

        self._show_message(
            "Skopírované",
            (
                "Zoznam výhercov bol skopírovaný "
                "do schránky."
            )
        )

    # =====================================
    # MINULÉ KOLO
    # =====================================

    def previous_cycle(self):

        amount_field = MDTextField(
            input_filter="float",
            mode="outlined"
        )

        amount_field.add_widget(
            MDTextFieldHintText(
                text="Vyzbieraná suma (€)"
            )
        )

        recipients_field = MDTextField(
            input_filter="int",
            mode="outlined"
        )

        recipients_field.add_widget(
            MDTextFieldHintText(
                text="Počet príjemcov"
            )
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

        cancel_button = MDButton(
            MDButtonText(text="ZRUŠIŤ"),
            style="text"
        )

        save_button = MDButton(
            MDButtonText(text="ULOŽIŤ"),
            style="text"
        )

        dialog = MDDialog(
            MDDialogHeadlineText(text="Minulé kolo"),
            MDDialogContentContainer(
                content,
                orientation="vertical"
            ),
            MDDialogButtonContainer(
                Widget(),
                cancel_button,
                save_button,
                spacing="8dp"
            ),
        )

        cancel_button.bind(
            on_release=lambda *args: dialog.dismiss()
        )

        save_button.bind(
            on_release=lambda *args: self._save_previous_cycle(
                amount_field.text,
                recipients_field.text,
                dialog
            )
        )

        dialog.open()

    # =====================================
    # ULOŽENIE MINULÉHO KOLA
    # =====================================

    def _save_previous_cycle(
        self,
        amount_text,
        recipients_text,
        dialog
    ):

        try:

            if (
                not amount_text.strip()
                or not recipients_text.strip()
            ):
                raise ValueError(
                    "Vyplň sumu aj počet príjemcov."
                )

            per_person = record_previous_cycle(
                amount_text.replace(",", "."),
                recipients_text
            )

            dialog.dismiss()

            self._show_message(
                "Minulé kolo uložené",
                (
                    f"Vyzbierané: "
                    f"{float(amount_text.replace(',', '.')):.2f} €\n"
                    f"Príjemcov: "
                    f"{int(recipients_text)}\n"
                    f"Na jedného: "
                    f"{per_person:.2f} €"
                )
            )

        except Exception as e:

            self._show_message(
                "Chyba",
                str(e)
            )

    # =====================================
    # HISTÓRIA
    # =====================================

    def history(self):
        self.manager.current = "history"
