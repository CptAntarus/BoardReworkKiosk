#################################################################################
#
#       - File: BRK_NoBoardScreen.py
#       - Author: Dylan Hendrix
#       - Discription: Screen used to show error messages if at any point
#                       there are no boards in the kiosk
#
################################################################################
#
#       - Comes From:   BRK_CheckInConfirm.py
#                       BRK_CheckOutBoard.py
#                       BRK_SelectCheckout.py
#
#       - Goes To:      BRK_StartScreen.py
#                       BRK_CheckOutBaord.py
#
#################################################################################

from kivymd.uix.screen import Screen
from kivymd.app import MDApp
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager


class NoBoardScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.delayedInit,0.1)
    

    def delayedInit(self, dt):
        self.ids.noBoardScreenTopBar.opacity = 1

        if GlobalScreenManager.noBoardsFlag == "NBR":
            self.ids.noBoardsMsg.text = "No Normal Board Reworks in Kiosk"
            GlobalScreenManager.noBoardsFlag = ""

        elif GlobalScreenManager.noBoardsFlag == "BGA":
            self.ids.noBoardsMsg.text = "No BGA Reworks in Kiosk"
            GlobalScreenManager.noBoardsFlag = ""

        elif GlobalScreenManager.noBoardsFlag == "NONE":
            self.ids.noBoardsMsg.text = "No Boards Match This Option"
            GlobalScreenManager.SCREEN_HIST.pop()
            GlobalScreenManager.noBoardsFlag = ""

        elif GlobalScreenManager.noBoardsFlag == "DOUBLE":
            self.ids.noBoardScreenTopBar.opacity = 0
            self.ids.noBoardsMsg.text = "Board Is already Logged in Dry Box"
            Clock.schedule_once(self.switchToStartScreen,4)
        
        elif GlobalScreenManager.noBoardsFlag == "DONE":
            self.ids.noBoardScreenTopBar.opacity = 0
            self.ids.noBoardsMsg.text = "Board Is Logged As Completed"
            Clock.schedule_once(self.switchToStartScreen,4)

        else:
            print("Error with noBoardsFlag assignment")


    def switchToStartScreen(self, dt):
        MDApp.get_running_app().reset
        MDApp.get_running_app().switchScreen("startScreen")
