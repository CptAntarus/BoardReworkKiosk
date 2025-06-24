from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from BRK_GSM import GlobalScreenManager

class CheckOutBoard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = MDApp.get_running_app().root

    def on_enter(self):
        pass