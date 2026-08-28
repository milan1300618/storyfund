import os

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
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

    # =====================================
    # UZAVRETIE KOLA
    # =====================================

    def close_cycle(self):

        try:

            # Uzavrie kolo:
            # - vyžrebuje výhercov
            # - uloží ich do Firebase
            # - vyčistí stories
            # - otvorí nové kolo
            force_new_cycle()

            # Načítame aktuálny archív
            archive = get_archive()

            winners = []

            if archive:

                last = archive[-1]

                winners = last.get(
                    "winners",
                    []
                )

            # Ochrana proti prípadnému neplatnému formátu
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

                MDDialog(
                    title="Kolo uzavreté",
                    text=(
                        "Kolo bolo úspešne uzavreté "
                        "a otvorilo sa nové kolo.\n\n"
                        "V tomto kole neboli vyžrebovaní "
                        "žiadni výhercovia."
                    )
                ).open()

        except Exception as e:

            MDDialog(
                title="Chyba pri uzatváraní kola",
                text=str(e)
            ).open()

    # =====================================
    # ZOBRAZENIE VÝHERCOV
    # =====================================

    def show_winners(self, winners):

        winners_text = "\n".join(winners)

        # Textové pole so zoznamom
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

        dialog = MDDialog(
            title=f"VÝHERCI ({len(winners)})",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="KOPÍROVAŤ ZOZNAM",
                    on_release=lambda x: self.copy_winners(
                        winners_text,
                        dialog
                    )
                ),
                MDFlatButton(
                    text="ZAVRIEŤ",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )

        dialog.open()

    # =====================================
    # KOPÍROVANIE VÝHERCOV
    # =====================================

    def copy_winners(self, winners_text, dialog):

        Clipboard.copy(winners_text)

        dialog.dismiss()

        MDDialog(
            title="Skopírované",
            text=(
                "Zoznam výhercov bol skopírovaný "
                "do schránky."
            )
        ).open()

    # =====================================
    # MINULÉ KOLO
    # =====================================

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
                        amount_field.text,
                        recipients_field.text,
                        dialog
                    )
                ),
            ],
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

            MDDialog(
                title="Minulé kolo uložené",
                text=(
                    f"Vyzbierané: "
                    f"{float(amount_text.replace(',', '.')):.2f} €\n"
                    f"Príjemcov: "
                    f"{int(recipients_text)}\n"
                    f"Na jedného: "
                    f"{per_person:.2f} €"
                )
            ).open()

        except Exception as e:

            MDDialog(
                title="Chyba",
                text=str(e)
            ).open()

    # =====================================
    # HISTÓRIA
    # =====================================

    def history(self):
        self.manager.current = "history"
