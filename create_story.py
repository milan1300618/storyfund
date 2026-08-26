# ======================================
# StoryFund v0.6
# File: screens/create_story.py
# ======================================

import random

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

from kivy.metrics import dp

from words import generate_words
from story_engine import generate_story

from backend import (
    save_story,
    can_add_story
)

from login import get_current_user

from settings_manager import get
from payment_check import check_payment


class CreateStoryScreen(MDScreen):

    def on_enter(self):

        self.words = generate_words()

        self.selected = []

        self.story = ""

        self.score = None

        self.attempts = 0

        self.build_screen()


    def build_screen(self):

        self.clear_widgets()

        root = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )

        title = MDLabel(
            text=f"Vyber {get('WORDS_TO_SELECT')} slová a vytvor príbeh",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )

        root.add_widget(title)

        if (not get("TEST_MODE")) and (not can_add_story(get_current_user())):

            info = MDLabel(
                text="V tomto kole už máš vytvorené maximálny počet príbehov.",
                halign="center"
            )

            root.add_widget(info)

            back = MDRaisedButton(
                text="SPÄŤ"
            )

            back.bind(
                on_release=self.back
            )

            root.add_widget(back)

            self.add_widget(root)

            return

        self.info = MDLabel(
            text=f"Vybrané: 0 / {get('WORDS_TO_SELECT')}",
            halign="center",
            size_hint_y=None,
            height=dp(35)
        )

        root.add_widget(self.info)

        self.word_box = MDGridLayout(
            cols=3,
            spacing=dp(6),
            adaptive_height=True,
            size_hint_x=1
        )

        for word in self.words:

            btn = MDRaisedButton(
                text=word,
                size_hint=(1, None),
                height=dp(34)
            )

            btn.bind(
                on_release=self.select_word
            )

            self.word_box.add_widget(btn)

        root.add_widget(self.word_box)

        self.generate_btn = MDRaisedButton(
            text="GENEROVAŤ PRÍBEH",
            disabled=True
        )

        self.generate_btn.bind(
            on_release=self.generate
        )

        root.add_widget(self.generate_btn)

        self.story_label = MDLabel(
            text="",
            valign="top"
        )

        root.add_widget(self.story_label)

        self.save_btn = MDRaisedButton(
            text="ULOŽIŤ",
            disabled=True
        )

        self.save_btn.bind(
            on_release=self.save
        )

        root.add_widget(self.save_btn)

        back = MDRaisedButton(
            text="SPÄŤ"
        )

        back.bind(
            on_release=self.back
        )

        root.add_widget(back)

        self.add_widget(root)


    def select_word(self, button):

        word = button.text

        if word in self.selected:

            self.selected.remove(word)

            button.md_bg_color = self.theme_cls.primary_color

        else:

            if len(self.selected) >= get("WORDS_TO_SELECT"):

                return

            self.selected.append(word)

            button.md_bg_color = (0, 0.7, 0.2, 1)

        self.info.text = (
            f"Vybrané: {len(self.selected)} / {get('WORDS_TO_SELECT')}"
        )

        self.generate_btn.disabled = (
            len(self.selected) != get("WORDS_TO_SELECT")
        )


    def generate(self, button):

        if len(self.selected) != get("WORDS_TO_SELECT"):

            return

        if self.attempts >= get("MAX_GENERATIONS"):

            return

        self.attempts += 1

        self.story = generate_story(
            self.selected
        )

        self.score = random.randint(
            get("MIN_AI_SCORE"),
            get("MAX_AI_SCORE")
        )

        text = self.story

        if get("SHOW_AI_SCORE"):

            text += (
                f"\n\n AI index: {self.score}%"
            )

        self.story_label.text = text

        self.save_btn.disabled = False

        if self.attempts >= get("MAX_GENERATIONS"):

            self.generate_btn.disabled = True

        else:

            zostava = (
                get("MAX_GENERATIONS")
                - self.attempts
            )

            self.generate_btn.text = (
                f"GENEROVAŤ ZNOVA ({zostava})"
            )
    def save(self, button):

        nik = get_current_user()

        if self.story == "":

            self.story_label.text = (
                "Najprv vygeneruj príbeh."
            )

            return

        if (not get("TEST_MODE")) and (not can_add_story(nik)):

            self.story_label.text = (
                "V tomto kole už máš vytvorené maximálny počet príbehov."
            )

            return

        if not get("TEST_MODE"):
            if not check_payment(nik):
                self.story_label.text = (
                    "Neregistruje sa dar (2€) na účte s týmto nickom za aktuálne kolo."
                )
                return

        save_story(
            nik,
            self.selected,
            self.story,
            self.score
        )

        text = " Príbeh bol uložený."


        self.story_label.text = text

        self.save_btn.disabled = True
        self.generate_btn.disabled = True


    def back(self, button):

        self.manager.current = "home"
