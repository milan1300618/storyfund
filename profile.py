# ======================================
# StoryFund v0.6
# screens/profile.py
# ======================================

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp

from login import get_current_user
from database import get_users, get_stories, get_archive


class ProfileScreen(MDScreen):

    def on_enter(self):
        self.clear_widgets()

        nik = get_current_user()

        # ======================================
        # ÚDAJE Z FIREBASE
        # ======================================
        users = get_users()
        stories = get_stories()
        history = get_archive()

        # ======================================
        # MOJE ÚDAJE
        # ======================================
        user = next(
            (u for u in users if u.get("nik") == nik),
            {}
        )

        reg = user.get("registered", "-")

        # Iba príbehy aktuálneho používateľa.
        mine = [
            s for s in stories
            if s.get("nik") == nik
        ]

        scores = [
            s.get("score", 0)
            for s in mine
            if isinstance(s.get("score"), (int, float))
        ]

        avg = (
            round(sum(scores) / len(scores), 1)
            if scores else 0
        )

        best = max(scores) if scores else 0

        # ======================================
        # ŠTATISTIKY STORYFUNDU
        # ======================================
        winners = 0
        total = 0.0

        for h in history:
            if not isinstance(h, dict):
                continue

            receivers = h.get("receivers", [])

            if isinstance(receivers, list):
                winners += len(receivers)

            try:
                total += float(h.get("fund", 0) or 0)
            except (TypeError, ValueError):
                pass

        # ======================================
        # ZOBRAZENIE
        # ======================================
        root = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(15)
        )

        txt = f'''[b]MÔJ PROFIL[/b]

Nick: {nik}
Registrovaný: {reg}
Dar uhradený pre aktuálne kolo: NIE

Počet mojich príbehov: {len(mine)}
Priemerné AI skóre: {avg} %
Najvyššie AI skóre: {best} %

[b]ŠTATISTIKY STORYFUNDU[/b]

Registrovaných používateľov: {len(users)}
Vytvorených príbehov: {len(stories)}
Uzavretých kôl: {len(history)}
Vyplatených odmien: {winners}
Celková vyplatená suma: {total:.2f} €'''

        root.add_widget(
            MDLabel(
                text=txt,
                markup=True,
                valign="top"
            )
        )

        back = MDRaisedButton(text="SPÄŤ")
        back.bind(on_release=self.back)
        root.add_widget(back)

        self.add_widget(root)

    def back(self, *args):
        self.manager.current = "home"
