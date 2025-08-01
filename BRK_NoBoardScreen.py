#################################################################################
#
#       - File: BRK_NoBoardScreen.py
#       - Author: Dylan Hendrix
#       - Discription: Screen used to show error messages if there are no
#                       boards in the kiosk
#
################################################################################
#
#       - Entries: BRK_CheckOutBoard.py
#                  BRK_CheckInConfirm.py
#                  BRK_AdminCheckout.py
#
#       - Exit:    BRK_StartScreen.py
#
#################################################################################

from kivymd.uix.screen import Screen
from kivymd.app import MDApp
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager


class NoBoardScreen(Screen):
    def on_enter(self):
        print("Entered 'NoBoardScreen'")
        Clock.schedule_once(self.delayedInit,0.1)
    
    def delayedInit(self, dt):
        self.ids.noBoardScreenTopBar.opacity = 1
        if GlobalScreenManager.noBoardsFlag == "NBR":
            self.ids.noBoardsMsg.text = "No Normal Reworks in Kiosk"
            GlobalScreenManager.noBoardsFlag = ""

        elif GlobalScreenManager.noBoardsFlag == "BGA":
            self.ids.noBoardsMsg.text = "No BGA Reworks in Kiosk"
            GlobalScreenManager.noBoardsFlag = ""

        elif GlobalScreenManager.noBoardsFlag == "NONE":
            self.ids.noBoardsMsg.text = "No Boards in Kiosk "
            GlobalScreenManager.SCREEN_HIST.pop()
            GlobalScreenManager.noBoardsFlag = ""

        elif GlobalScreenManager.noBoardsFlag == "DOUBLE":
            self.ids.noBoardScreenTopBar.opacity = 0
            self.ids.noBoardsMsg.text = "Board Is already Logged in Dry Box"
            Clock.schedule_once(self.switchToStartScreen,4)
            
        else:
            print("Error with noBoardsFlag assignment")

    def switchToStartScreen(self, dt):
        MDApp.get_running_app().reset
        MDApp.get_running_app().switchScreen("startScreen")
