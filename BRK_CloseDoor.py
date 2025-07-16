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
            self.ids.closeDoorMsg.text = 'Place Board In Kiosk @ ' + "( row " + str(GlobalScreenManager.CURRENT_POS_X) + ", " + " col " + str(GlobalScreenManager.CURRENT_POS_Y) + " )"

            # self.ids.boardLocationX.text = "( row " + str(GlobalScreenManager.CURRENT_POS_X) + ", "
            # self.ids.boardLocationY.text = " col " + str(GlobalScreenManager.CURRENT_POS_Y) + " )"

        elif GlobalScreenManager.SCREEN_HIST[-1] == 'checkOutConfirm':
            data = GlobalScreenManager.BOARD_CHECKOUT
            self.ids.closeDoorMsg.text = 'Remove Board From Kiosk @ ' + "( row " + str(data[8]) + ", " + " col " + str(data[9]) + " )"
            # self.ids.boardLocationX.text = "( row " + str(data[8]) + ", "
            # self.ids.boardLocationY.text = " col " + str(data[9]) + " )"
        else:
            print("Error selecting text")


        MDApp.get_running_app().reset(0.1)
        Clock.schedule_once(lambda dt: MDApp.get_running_app().switchScreen('startScreen'), 120)
