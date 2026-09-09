import os

from kivy.lang import Builder
from kivy.uix.widget import Widget

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonText

import settings_manager

Builder.load_file(
    os.path.join(os.path.dirname(__file__), "settings.kv")
)


class SettingsScreen(MDScreen):

    def on_pre_enter(self):
        s = settings_manager.load_settings()

        self.ids.test_mode.active = s.get('TEST_MODE', False)
        self.ids.max_stories.text = str(
            s.get('MAX_STORIES_PER_CYCLE', 3)
        )
        self.ids.max_generations.text = str(
            s.get('MAX_GENERATIONS', 3)
        )
        self.ids.words_to_show.text = str(
            s.get('WORDS_TO_SHOW', 8)
        )
        self.ids.words_to_select.text = str(
            s.get('WORDS_TO_SELECT', 4)
        )
        self.ids.min_ai_score.text = str(
            s.get('MIN_AI_SCORE', 70)
        )
        self.ids.max_ai_score.text = str(
            s.get('MAX_AI_SCORE', 100)
        )
        self.ids.show_ai_score.active = s.get(
            'SHOW_AI_SCORE',
            True
        )
        self.ids.winners_per_cycle.text = str(
            s.get('WINNERS_PER_CYCLE', 12)
        )

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

    def save_settings(self):
        try:
            settings_manager.set(
                'TEST_MODE',
                self.ids.test_mode.active
            )
            settings_manager.set(
                'MAX_STORIES_PER_CYCLE',
                int(self.ids.max_stories.text)
            )
            settings_manager.set(
                'MAX_GENERATIONS',
                int(self.ids.max_generations.text)
            )
            settings_manager.set(
                'WORDS_TO_SHOW',
                int(self.ids.words_to_show.text)
            )
            settings_manager.set(
                'WORDS_TO_SELECT',
                int(self.ids.words_to_select.text)
            )
            settings_manager.set(
                'MIN_AI_SCORE',
                int(self.ids.min_ai_score.text)
            )
            settings_manager.set(
                'MAX_AI_SCORE',
                int(self.ids.max_ai_score.text)
            )
            settings_manager.set(
                'SHOW_AI_SCORE',
                self.ids.show_ai_score.active
            )
            settings_manager.set(
                'WINNERS_PER_CYCLE',
                int(self.ids.winners_per_cycle.text)
            )

            self._show_message(
                'Nastavenia',
                'Nastavenia boli úspešne uložené.'
            )

        except Exception as e:
            self._show_message(
                'Chyba',
                str(e)
            )

    def back(self):
        self.manager.current = 'admin'
