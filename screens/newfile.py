# ======================================
# StoryFund v0.5
# screens/home.py
# ======================================

import webbrowser

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard

from kivy.metrics import dp
from kivy.clock import Clock

from backend import load_feed
from screens.login import get_current_user


TRANSPARENT_ACCOUNT = (
    "https://www.unicreditbank.sk/sk/ostatne/"
    "transparentny-ucet.html?"
    "IBAN=SK5611110000001491048088"
)


class HomeScreen(MDScreen):

    def on_enter(self):
        self.build_screen()

    def build_screen(self):

        self.clear_widgets()

        root = MDBoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(15)
        )

        # =====================================
        # Horná pevná časť
        # =====================================

        title = MDLabel(
            text="StoryFund",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(55)
        )

        root.add_widget(title)

        user_label = MDLabel(
            text=f"Vitaj, {get_current_user()} 👋",
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
        new_story_btn.bind(
            on_release=self.create_story
        )
        buttons.add_widget(new_story_btn)

        profile_btn = MDRaisedButton(
            text="PROFIL",
            size_hint_x=1
        )
        profile_btn.bind(
            on_release=self.profile
        )
        buttons.add_widget(profile_btn)

        logout_btn = MDRaisedButton(
            text="ODHLÁSIŤ",
            size_hint_x=1
        )
        logout_btn.bind(
            on_release=self.logout
        )
        buttons.add_widget(logout_btn)

        root.add_widget(buttons)

        account_btn = MDRaisedButton(
            text="💰 TRANSPARENTNÝ ÚČET",
            size_hint=(1, None),
            height=dp(42)
        )
        account_btn.bind(
            on_release=self.open_account
        )
        root.add_widget(account_btn)

        # =====================================
        # Feed (pripravený na budúce auto-scroll)
        # =====================================

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
                    text=f"⭐ AI index: {s['score']} %",
                    size_hint_y=None,
                    adaptive_height=True
                )

                card.add_widget(author)
                card.add_widget(story)
                card.add_widget(score)

                card.bind(
                    width=lambda *_,
                    lbl=story: setattr(lbl, "text_size", (card.width - dp(30), None))
                )

                self.feed.add_widget(card)

        self.scroll.add_widget(self.feed)
        root.add_widget(self.scroll)

        # medzera pred spodným panelom
        root.add_widget(
            MDLabel(
                text="",
                size_hint_y=None,
                height=dp(16)
            )
        )

        # =====================================
        # Súhrn posledného kola (pevný spodný panel)
        # =====================================

        summary = MDRaisedButton(
            text="💰 MINULOTÝŽDŇOVÁ ZBIERKA
Vyzbierané: 245,60 €
👥 Odmenených autorov: 12   📅 13.07.2026",
            size_hint=(1, None),
            height=dp(88)
        )

        root.add_widget(summary)

        self.add_widget(root)

        Clock.unschedule(self.auto_scroll)
        Clock.schedule_interval(self.auto_scroll, 0.03)

    # =====================================
    # Transparentný účet
    # (zostáva zachovaný pre budúce použitie)
    # =====================================

    def open_account(self, *args):

        webbrowser.open(
            TRANSPARENT_ACCOUNT
        )

    # =====================================
    # Nový príbeh
    # =====================================

    def create_story(self, *args):

        self.manager.current = "create_story"

    # =====================================
    # Profil
    # =====================================

    def profile(self, *args):

        self.manager.current = "profile"

    # =====================================
    # Odhlásenie
    # =====================================

    def logout(self, *args):

        self.manager.current = "login"

    # =====================================
    # Automatické pomalé rolovanie
    # =====================================

    def auto_scroll(self, dt):
        if not hasattr(self, "scroll"):
            return
        step = 0.0005
        y = self.scroll.scroll_y
        self.scroll.scroll_y = 1.0 if y <= 0 else y - step
