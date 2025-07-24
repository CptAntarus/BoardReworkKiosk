#################################################################################
#
#       - File: BRK_CloseDoor.py
#       - Author: Dylan Hendrix
#       - Discription: This screen prompts the user to to take the board
#                       out or put a board into the kiosk. It returns to
#                       main after 2mins or via the 'Done' button
#
################################################################################
#
#       - Entries: BRK_CheckInConfirm.py
#                  BRK_CheckoutConfirm.py
#                  BRK_AdminConfirm.py
#                  BRK_AdminEnterUser.py
#
#       - Exit:    BRK_StartScreen.py
#
#################################################################################

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager


class CloseDoor(Screen):
    def on_enter(self):
        Clock.schedule_once(self.delayedInit, 0.1)


    def delayedInit(self, dt):
        print(GlobalScreenManager.SCREEN_HIST[-1])
        self.flag = True
        self.countDown = 120

        # Edit message according to operation
        if GlobalScreenManager.SCREEN_HIST[-1] == 'checkInConfirm':
            self.ids.closeDoorMsg.text = 'Place Board In Kiosk @ ' + "( row " + str(GlobalScreenManager.CURRENT_POS_X) + ", " + " col " + str(GlobalScreenManager.CURRENT_POS_Y) + " )"
        elif GlobalScreenManager.SCREEN_HIST[-1] == 'checkOutConfirm':
            data = GlobalScreenManager.BOARD_CHECKOUT
            self.ids.closeDoorMsg.text = 'Remove Board From Kiosk @ ' + "( row " + str(data[8]) + ", " + " col " + str(data[9]) + " )"
        else:
            print("Error selecting text")

        self.updateCountdown(0)
        if hasattr(self, 'countdown_event'):
            self.countdown_event.cancel()

        self.countdown_event = Clock.schedule_interval(self.updateCountdown, 1)
        self.timeOut()


    def updateCountdown(self, dt):
        if self.countDown > 0:
            mins = self.countDown // 60
            sec = self.countDown % 60

            self.ids.doorCountDown.text = f"{mins}:{sec:02}"
            self.countDown -= 1
        else:
            self.ids.doorCountDown.text = "00:00"
            if hasattr(self, 'countdown_event'):
                self.countdown_event.cancel()


    # Return to start screen and cancel timer
    def doneBtn(self):
        MDApp.get_running_app().reset(0.1)
        self.flag = False
        if hasattr(self, 'timeout_event'):
            self.timeout_event.cancel()
        if hasattr(self, 'countdown_event'):
            self.countdown_event.cancel()
        MDApp.get_running_app().switchScreen('startScreen')


    def timeOut(self):
        self.timeout_event = Clock.schedule_once(self.autoSwitch, 120)


    # Return to start screen if timer expires
    def autoSwitch(self, dt):
        if self.flag:
            if hasattr(self, 'countdown_event'):
                self.countdown_event.cancel()
            MDApp.get_running_app().reset(0.1)
            MDApp.get_running_app().switchScreen('startScreen')


    # Cancel timer on leave to avoid activation later
    def on_leave(self):
        if hasattr(self, 'countdown_event'):
            self.countdown_event.cancel()
        if hasattr(self, 'timeout_event'):
            self.timeout_event.cancel()
