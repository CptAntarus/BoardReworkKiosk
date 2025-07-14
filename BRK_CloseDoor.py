from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager, GSM

class CloseDoor(Screen):
    def on_enter(self):
        print("Made it to CloseDoor==================")
        Clock.schedule_once(self.delayedInit, 0.1)


    def delayedInit(self, dt):
        print(GlobalScreenManager.SCREEN_HIST[-1])

        if GlobalScreenManager.SCREEN_HIST[-1] == 'checkInConfirm':
            self.ids.closeDoorMsg.text = 'Place Board In Kiosk'
        elif GlobalScreenManager.SCREEN_HIST[-1] == 'checkOutConfirm':
            self.ids.closeDoorMsg.text = 'Remove Board From Kiosk'
        else:
            print("Error selecting text")

        self.otherstuff()

    def otherstuff(self):
        Clock.schedule_once(lambda dt: MDApp.get_running_app().switchScreen('startScreen'), 30)
