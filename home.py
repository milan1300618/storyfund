# ======================================
# StoryFund v0.5
# screens/home.py
# ======================================

import os
import webbrowser

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard

from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivy.metrics import dp
from kivy.clock import Clock

from backend import load_feed
from login import get_current_user
from database import get_archive, get_stories
from cycle import get_fund


TRANSPARENT_ACCOUNT = (
    "https://www.unicreditbank.sk/sk/ostatne/"
    "transparentny-ucet.html?"
    "IBAN=SK5611110000001491048088"
)

QR_MINI_IMAGE = "qr_mini.jpg"

PAYMENT_IBAN = "SK5611110000001491048088"
PAYMENT_AMOUNT = 2.00
PAYMENT_BENEFICIARY = "Transparentny fond"


class ClickableImage(ButtonBehavior, Image):
    pass


class HomeScreen(MDScreen):

    def on_enter(self):
        self.build_screen()

    def get_summary_data(self):
        fund = get_fund()
        archive = get_archive()

        # Pocet darcov = pocet unikatnych NIKov,
        # ktore maju v aktualnom kole ulozeny pribeh.
        stories = get_stories()
        donors = len({
            str(s.get("nik", "")).strip()
            for s in stories
            if str(s.get("nik", "")).strip()
        })

        last_fund = 0.0
        last_winners = 12
        last_per_person = 0.0

        if archive:
            last = archive[-1]
            last_fund = float(last.get("fund", 0) or 0)

            participants = last.get("participants", None)
            if participants is None:
                participants = last.get("winners", 12)

            try:
                last_winners = int(participants)
            except (TypeError, ValueError):
                last_winners = 12

            try:
                last_per_person = float(
                    last.get("amount_per_person", 0) or 0
                )
            except (TypeError, ValueError):
                last_per_person = 0.0

            if last_per_person <= 0 and last_winners > 0:
                last_per_person = last_fund / last_winners

        return {
            "fund": fund,
            "donors": donors,
            "last_fund": last_fund,
            "last_winners": last_winners,
            "last_per_person": last_per_person,
        }

    def build_screen(self):
        self.clear_widgets()
        stats = self.get_summary_data()

        root = MDBoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(15)
        )

        title = MDLabel(
            text="StoryFund",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(55)
        )
        root.add_widget(title)

        user_label = MDLabel(
            text=f"Vitaj, {get_current_user()} ",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        root.add_widget(user_label)

        buttons = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        new_story_btn = MDRaisedButton(
            text="NOVÝ PRÍBEH",
            size_hint_x=1
        )
        new_story_btn.bind(on_release=self.create_story)
        buttons.add_widget(new_story_btn)

        profile_btn = MDRaisedButton(
            text="PROFIL",
            size_hint_x=1
        )
        profile_btn.bind(on_release=self.profile)
        buttons.add_widget(profile_btn)

        logout_btn = MDRaisedButton(
            text="ODHLÁSIŤ",
            size_hint_x=1
        )
        logout_btn.bind(on_release=self.logout)
        buttons.add_widget(logout_btn)

        root.add_widget(buttons)

        account_area = RelativeLayout(
            size_hint=(1, None),
            height=dp(42)
        )

        account_btn = MDRaisedButton(
            text=" TRANSPARENTNÝ ÚČET",
            size_hint=(1, 1)
        )
        account_btn.bind(on_release=self.open_account)
        account_area.add_widget(account_btn)

        mini_qr = ClickableImage(
            source=QR_MINI_IMAGE,
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            pos_hint={"right": 0.985, "center_y": 0.5}
        )
        mini_qr.bind(on_release=self.open_qr_fullscreen)
        account_area.add_widget(mini_qr)

        root.add_widget(account_area)

        self.scroll = MDScrollView()

        self.feed = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None,
            adaptive_height=True,
            padding=(0, 0, 0, dp(10))
        )

        stories = load_feed()

        if not stories:
            self.feed.add_widget(
                MDLabel(
                    text="Zatiaľ nie sú žiadne príbehy.",
                    halign="center",
                    size_hint_y=None,
                    height=dp(50)
                )
            )
        else:
            for s in stories:
                card = MDCard(
                    orientation="vertical",
                    padding=dp(15),
                    spacing=dp(10),
                    radius=[15],
                    size_hint_y=None,
                    adaptive_height=True
                )

                author = MDLabel(
                    text=f"👤 {s['nik']}",
                    bold=True,
                    size_hint_y=None,
                    adaptive_height=True
                )

                story = MDLabel(
                    text=s["story"],
                    size_hint_y=None,
                    adaptive_height=True
                )

                score = MDLabel(
                    text=f" AI index: {s['score']} %",
                    size_hint_y=None,
                    adaptive_height=True
                )

                card.add_widget(author)
                card.add_widget(story)
                card.add_widget(score)

                card.bind(
                    width=lambda *_, lbl=story:
                    setattr(
                        lbl,
                        "text_size",
                        (card.width - dp(30), None)
                    )
                )

                self.feed.add_widget(card)

        self.scroll.add_widget(self.feed)
        root.add_widget(self.scroll)

        root.add_widget(
            MDLabel(
                text="",
                size_hint_y=None,
                height=dp(16)
            )
        )

        summary = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height=dp(175),
            padding=dp(12),
            spacing=dp(5),
            radius=[12],
            md_bg_color=(0.15, 0.35, 0.75, 1)
        )

        summary.add_widget(
            MDLabel(
                text="PREHĽAD STORYFUNDU",
                font_style="H6",
                halign="center",
                size_hint_y=None,
                height=dp(22)
            )
        )

        summary.add_widget(
            MDLabel(
                text=(
                    f"Fond aktuálneho kola: {stats['fund']:.2f} €\n"
                    f"Počet darcov: {stats['donors']}"
                ),
                halign="center",
                size_hint_y=None,
                height=dp(38)
            )
        )

        summary.add_widget(
            MDLabel(
                text=(
                    f" MINULÉ KOLO\n"
                    f" Rozdelené medzi: {stats['last_winners']} ľudí\n"
                    f" Darované a rozdané: {stats['last_fund']:.2f} €\n"
                    f" Na NIK: {stats['last_per_person']:.2f} €"
                ),
                halign="center",
                size_hint_y=None,
                height=dp(82)
            )
        )

        root.add_widget(summary)
        self.add_widget(root)

        Clock.unschedule(self.auto_scroll)
        Clock.schedule_interval(self.auto_scroll, 0.03)

    def open_qr_fullscreen(self, *args):
        try:
            import pay_by_square
            import segno

            nick = str(get_current_user()).strip()
            variable_symbol = nick

            if variable_symbol.upper().startswith("SF"):
                variable_symbol = variable_symbol[2:]

            variable_symbol = variable_symbol.strip()

            if not variable_symbol:
                raise ValueError("NIK je prázdny.")

            code = pay_by_square.generate(
                amount=PAYMENT_AMOUNT,
                iban=PAYMENT_IBAN,
                currency="EUR",
                variable_symbol=variable_symbol,
                beneficiary_name=PAYMENT_BENEFICIARY
            )

            qr_path = os.path.join(
                self.get_app_qr_directory(),
                f"qr_payment_{variable_symbol}.png"
            )

            qr = segno.make_qr(code)
            qr.save(qr_path, scale=10)

            modal = ModalView(
                size_hint=(1, 1),
                auto_dismiss=False,
                background_color=(0, 0, 0, 1)
            )

            full_qr = ClickableImage(
                source=qr_path,
                size_hint=(1, 1),
                allow_stretch=True,
                keep_ratio=True
            )

            full_qr.bind(on_release=modal.dismiss)
            modal.add_widget(full_qr)
            modal.open()

        except Exception as e:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDFlatButton

            dialog = MDDialog(
                title="QR chyba",
                text=f"{type(e).__name__}: {e}",
                buttons=[MDFlatButton(text="OK")]
            )

            dialog.buttons[0].bind(on_release=dialog.dismiss)
            dialog.open()

    def get_app_qr_directory(self):
        from kivy.app import App
        directory = App.get_running_app().user_data_dir
        os.makedirs(directory, exist_ok=True)
        return directory

    def open_account(self, *args):
        webbrowser.open(TRANSPARENT_ACCOUNT)

    def create_story(self, *args):
        self.manager.current = "create_story"

    def profile(self, *args):
        self.manager.current = "profile"

    def logout(self, *args):
        self.manager.current = "login"

    def auto_scroll(self, dt):
        if not hasattr(self, "scroll"):
            return

        step = 0.0010
        y = self.scroll.scroll_y
        self.scroll.scroll_y = 1.0 if y <= 0 else y - step
