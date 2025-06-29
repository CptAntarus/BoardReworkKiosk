# KivyMD Imports
from kivymd.app import MDApp
from kivymd.uix.textfield import textfield
from kivymd.uix.anchorlayout import AnchorLayout
from kivymd.uix.button import MDIconButton

# Kivy Imports
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition

from kivy.lang import Builder
Builder.load_file("BRK_Format.kv")


from BRK_GSM import GlobalScreenManager
from BRK_StartScreen import StartScreen
from BRK_InOutScreen import InOutScreen
from BRK_CheckInBoard import CheckInBoard
from BRK_CheckOutBoard import CheckOutBoard
from BRK_CheckInConfirm import CheckInConfirmScreen


class BRKGui(MDApp):
    def build(self):
        self.sm = GlobalScreenManager()
        self.sm.add_widget(StartScreen(name='startScreen'))
        self.sm.add_widget(InOutScreen(name='inOutScreen'))
        self.sm.add_widget(CheckInBoard(name='checkInBoard'))
        self.sm.add_widget(CheckOutBoard(name='checkOutBoard'))
        self.sm.add_widget(CheckInConfirmScreen(name='checkInConfirm'))

        self.sm.transition = NoTransition()
        self.theme_cls.theme_style = 'Dark'
        self.switchScreen('startScreen') #checkInConfirm

        return self.sm
    

    def switchScreen(self, newScreen):
        GlobalScreenManager.SCREEN_HIST.append(self.sm.current)
        self.sm.current = newScreen

    def backButton(self, *args):
        if GlobalScreenManager.SCREEN_HIST:
            self.sm.current = GlobalScreenManager.SCREEN_HIST.pop()

    def reset(self,dt):
        GlobalScreenManager.CURRENT_USER = 0
        GlobalScreenManager.CURRENT_MO = 0
        GlobalScreenManager.CURRENT_BID = 0
        GlobalScreenManager.CURRENT_PRIORITY = 0
        GlobalScreenManager.HASH_KEY = 0
        GlobalScreenManager.PREVIOUS_SCREEN = ""

        self.sm.get_screen('startScreen').ids.EmpID.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInMO.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInBarCode.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInPriority.text = ""

        GlobalScreenManager.SCREEN_HIST.clear()

if __name__ == '__main__':
    BRKGui().run()
