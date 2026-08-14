# ======================================
# StoryFund v0.5
# app.py
# ======================================

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from screens.history import HistoryScreen
from screens.settings import SettingsScreen
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.create_story import CreateStoryScreen
from screens.profile import ProfileScreen
from screens.admin import AdminScreen
from screens.users import UsersScreen
from screens.user_detail import UserDetailScreen
from screens.new_user import NewUserScreen


class StoryFundApp(MDApp):

    def build(self):
        self.title = "StoryFund"

        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CreateStoryScreen(name="create_story"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(UsersScreen(name="users"))
        sm.add_widget(UserDetailScreen(name="user_detail"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(HistoryScreen())
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(NewUserScreen(name="new_user"))

        sm.current = "login"
        return sm


if __name__ == "__main__":
    StoryFundApp().run()
