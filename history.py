import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem

from database import get_archive

Builder.load_file(os.path.join(os.path.dirname(__file__), "history.kv"))


class HistoryScreen(MDScreen):

    def on_pre_enter(self):
        self.load_history()

    def load_history(self):
        self.ids.history_list.clear_widgets()

        archive = get_archive()

        archive.reverse()

        for cycle in archive:

            fund = cycle.get("fund", 0)
            people = cycle.get("people", cycle.get("users", cycle.get("count", 0)))

            try:
                fund = float(fund)
            except (TypeError, ValueError):
                fund = 0

            try:
                people = int(people)
            except (TypeError, ValueError):
                people = 0

            if people > 0:
                per_person = fund / people
                per_person_text = f"{per_person:.2f} €"
            else:
                per_person_text = "—"

            item = TwoLineListItem(
                text="Minulé kolo",
                secondary_text=(
                    f"Vyzbierané: {fund:.2f} €   |   "
                    f"Ľudí: {people}   |   "
                    f"Po: {per_person_text}"
                )
            )

            self.ids.history_list.add_widget(item)

    def back(self):
        self.manager.current = "admin"