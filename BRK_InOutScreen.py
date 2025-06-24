from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from BRK_GSM import GlobalScreenManager, GSM

class InOutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = GSM()

    def on_enter(self):
        pass