import sqlite3
import re

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
from BRK_CheckOutConfirm import CheckOutConfirm


class BRKGui(MDApp):
    def build(self):
        self.sm = GlobalScreenManager()
        self.sm.add_widget(StartScreen(name='startScreen'))
        self.sm.add_widget(InOutScreen(name='inOutScreen'))
        self.sm.add_widget(CheckInBoard(name='checkInBoard'))
        self.sm.add_widget(CheckOutBoard(name='checkOutBoard'))
        self.sm.add_widget(CheckInConfirmScreen(name='checkInConfirm'))
        self.sm.add_widget(CheckOutConfirm(name='checkOutComfirm'))

        self.populateDoorsList()

        self.sm.transition = NoTransition()
        self.theme_cls.theme_style = 'Dark'
        self.switchScreen('startScreen') #inOutScreen

        return self.sm
    
    def populateDoorsList(self):
        conn = sqlite3.connect("KioskDB.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM checkins")
            rows = cursor.fetchall()

            numRows = len(GlobalScreenManager.KIOSK_BOXES)
            numCols = len(GlobalScreenManager.KIOSK_BOXES[0]) if numRows > 0 else 0
            index = 0

            for row in rows:
                if index >= numRows * numCols:
                    print("Too many entires in DB. No slots left")
                else:
                    data = str(row)
                    pattern = r"(?:'([^']*)'|(\d+(?:\.\d+)?))"
                    matches = re.findall(pattern, data)
                    values = [group[0] if group[0] else group[1] for group in matches]

                    hashKey = values[1]

                    print(f"values[8]: {values[8]}:::::::::values[9]: {values[9]}")

                    # values[8 and 9] are the index of the slot the board was previously in
                    GlobalScreenManager.KIOSK_BOXES[int(values[8])][int(values[9])] = hashKey
                    index += 1

        except Exception as e:
            print("Error repopulating kiosk boxes:",e)

        finally:
            print(GlobalScreenManager.KIOSK_BOXES)
            conn.close()

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
        GlobalScreenManager.BOARD_CHECKOUT = 0

        self.sm.get_screen('startScreen').ids.EmpID.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInMO.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInBarCode.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInPriority.text = ""

        GlobalScreenManager.SCREEN_HIST.clear()

if __name__ == '__main__':
    BRKGui().run()
