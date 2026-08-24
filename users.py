import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from backend import list_users
from settings_manager import get

Builder.load_file(os.path.join(os.path.dirname(__file__), "users.kv"))

class UsersScreen(MDScreen):
    def on_pre_enter(self):
        self.all_users=list_users()
        self.filter_users("")

    def filter_users(self,text):
        self.ids.users_list.clear_widgets()
        t=text.upper().strip()
        shown=0
        for u in self.all_users:
            if t and t not in u["nik"].upper():
                continue
            shown+=1
            item=OneLineListItem(text=f"{u['nik']}   ({'AKTÍVNY' if u.get('active',True) else 'BLOKOVANÝ'})   {u.get('stories_count',0)}/{get('MAX_STORIES_PER_CYCLE')}")
            item.bind(on_release=lambda x,user=u:self.open_user(user))
            self.ids.users_list.add_widget(item)
        self.ids.count_label.text=f"Používateľov: {len(self.all_users)} | Zobrazených: {shown}"

    def open_user(self,user):
        s=self.manager.get_screen("user_detail")
        s.show_user(user)
        self.manager.current="user_detail"

    def back(self):
        self.manager.current="admin"
