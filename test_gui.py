from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


class Test(MDApp):

    def build(self):
        return MDLabel(
            text="Funguje KivyMD",
            halign="center"
        )


Test().run()