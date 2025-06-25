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
        self.sm.current = 'startScreen' #checkInConfirm

        return self.sm
    

    def switchScreen(self, newScreen, prevScreen):
        self.sm.PREVIOUS_SCREEN = prevScreen
        self.sm.current = newScreen

    def backButton(self, prevScreen):
        self.sm.current = self.sm.PREVIOUS_SCREEN


if __name__ == '__main__':
    BRKGui().run()
