#################################################################################
#
#       - File: BRK_StartScreen.py
#       - Author: Dylan Hendrix
#       - Discription: Screen shows the login screen and controls validation
#
################################################################################
#
#       - Entries: BRK_Main.py
#                  BRK_CloseDoor.py
#
#       - Exit:    BRK_StartScreen.py
#
#################################################################################

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager, GSM


class StartScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(MDApp.get_running_app().reset,0.1)
        Clock.schedule_once(self.set_focus, 0.1)


    def set_focus(self, dt):
        self.ids.EmpID.focus = True


    def validateUsr(self, uNum):
        if uNum in GlobalScreenManager.USERS:
            print(f"Valid user: {uNum}")
            GlobalScreenManager.CURRENT_USER = self.ids.EmpID.text.strip()
            print(f"uNum: {uNum}")
            MDApp.get_running_app().switchScreen('inOutScreen')
            
        else:
            print("Invalid User")
            self.ids.EmpID.text=""
            Clock.schedule_once(self.clearInput,0.1)


    def clearInput(self, dt):
        self.ids.EmpID.text=""
        self.ids.EmpID.focus=True
