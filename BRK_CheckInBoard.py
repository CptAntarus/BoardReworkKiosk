#################################################################################
#
#       - File: BRK_CheckInBoard.py
#       - Author: Dylan Hendrix
#       - Discription: This screen controls the board input process and 
#                       validates entered of data.
#
################################################################################
#
#       - Entry:   BRK_InOutScreen.py
#
#       - Exit:    BRK_CheckInConfirm.py
#
#################################################################################

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import re

from BRK_GSM import GlobalScreenManager


class CheckInBoard(Screen):
    def on_enter(self):
        # Rest Text inputs
        self.ids.boardInMO.text = ""
        self.ids.boardInBarCode.text = ""
        self.ids.boardInPriority.text = ""
        self.ids.boardInRWType.text = ""

        self.ids.boardInBarCode.opacity = 0
        self.ids.boardInPriority.opacity = 0
        self.ids.boardInRWType.opacity = 0

        Clock.schedule_once(self.set_focus, 0.1)


    def set_focus(self, dt):
        self.ids.boardInMO.focus = True


    def validateMO(self, textInput):
        pattern = r"\d{10}"

        if re.fullmatch(pattern, textInput):
            GlobalScreenManager.CURRENT_MO = textInput

            # Activate Board ID text box
            self.ids.boardInBarCode.opacity = 1
            self.ids.boardInBarCode.disabled = False
            self.ids.boardInBarCode.focus = True

        else:
            print("Invalid MO")
            self.ids.boardInMO.text=""
            Clock.schedule_once(self.clearInputMO,0.1)
    

    def validateBarCode(self, textInput):
        pattern = r"\d{6}-\d{3}/\w{1}/\w{2}\d{4}"

        if re.fullmatch(pattern, textInput):
            GlobalScreenManager.CURRENT_BID = textInput

            # Activate Priority text box
            self.ids.boardInPriority.opacity = 1
            self.ids.boardInPriority.disabled = False
            self.ids.boardInPriority.focus = True
        
        else:
            print("Invalid Input")
            self.ids.boardInBarCode.text = ""
            Clock.schedule_once(self.clearInputBarCode, 0.1)


    def validatePriority(self, textInput):
        pattern = r"priority [0-9]"

        if re.fullmatch(pattern, textInput):
            if textInput.lower() == "priority 1":
                GlobalScreenManager.CURRENT_PRIORITY = 1
                print(f"GSM Priority: {GlobalScreenManager.CURRENT_PRIORITY}")
            elif textInput.lower() == "priority 2":
                GlobalScreenManager.CURRENT_PRIORITY = 2
                print(f"GSM Priority: {GlobalScreenManager.CURRENT_PRIORITY}")
            elif textInput.lower() == "priority 3":
                GlobalScreenManager.CURRENT_PRIORITY = 3
                print(f"GSM Priority: {GlobalScreenManager.CURRENT_PRIORITY}")

            # Activate Rework Type text box
            self.ids.boardInRWType.opacity = 1
            self.ids.boardInRWType.disabled = False
            self.ids.boardInRWType.focus = True
        
        else:
            print("Invalid Input")
            self.ids.boardInPriority.text = ""
            Clock.schedule_once(self.clearInputPriority, 0.1)


    def validateRWType(self, textInput):
        if textInput.lower() == "rwtype bga":
            GlobalScreenManager.CURRENT_RW_TYPE = "BGA"
            print(f"GSM RW Type: {GlobalScreenManager.CURRENT_RW_TYPE}")
            MDApp.get_running_app().switchScreen('checkInConfirm')

        elif textInput.lower() == "rwtype nbr":    # nbr => normal board rework
            GlobalScreenManager.CURRENT_RW_TYPE = "NBR"
            print(f"GSM RW Type: {GlobalScreenManager.CURRENT_RW_TYPE}")
            MDApp.get_running_app().switchScreen('checkInConfirm')

        else:
            print("Invalid Input")
            self.ids.boardInRWType.text = ""
            Clock.schedule_once(self.clearInputRWType, 0.1)


    def clearInputMO(self, dt):
        self.ids.boardInMO.text=""
        self.ids.boardInMO.focus=True


    def clearInputBarCode(self, dt):
        self.ids.boardInBarCode.text=""
        self.ids.boardInBarCode.focus=True


    def clearInputPriority(self, dt):
        self.ids.boardInPriority.text = ""
        self.ids.boardInPriority.focus = True


    def clearInputRWType(self, dt):
        self.ids.boardInRWType.text = ""
        self.ids.boardInRWType.focus = True
