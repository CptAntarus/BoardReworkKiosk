from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager, GSM

class CloseDoor(Screen):
    def on_enter(self):
        print("Made it to CloseDoor==================")
        Clock.schedule_once(lambda dt: MDApp.get_running_app().switchScreen('startScreen'), 3)
