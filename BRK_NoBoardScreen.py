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
#                  BRK_AdminCheckout.py
#
#       - Exit:    BRK_StartScreen.py
#
#################################################################################

from kivymd.uix.screen import Screen

from BRK_GSM import GlobalScreenManager


class NoBoardScreen(Screen):
    def on_enter(self):
        print("Entered 'NoBoardScreen'")

        if GlobalScreenManager.noBoardsFlag == "NBR":
            self.ids.noBoardsMsg.text = "No Normal Reworks in Kiosk"
            GlobalScreenManager.noBoardsFlag = ""
        elif GlobalScreenManager.noBoardsFlag == "BGA":
            self.ids.noBoardsMsg.text = "No BGA Reworks in Kiosk"
            GlobalScreenManager.noBoardsFlag = ""
        elif GlobalScreenManager.noBoardsFlag == "NONE":
            self.ids.noBoardsMsg.text = "No Boards in Kiosk"
            GlobalScreenManager.SCREEN_HIST.pop()
            GlobalScreenManager.noBoardsFlag = ""
        else:
            print("Error with noBoardsFlag assignment")
