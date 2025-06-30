from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from BRK_GSM import GlobalScreenManager
import sqlite3

class CheckOutBoard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = MDApp.get_running_app().root

    def on_enter(self):
        self.ids.BoardReworkBtn.opacity = 0
        self.ids.BGAReworkBtn.opacity = 0
        self.ids.NoAccessMsg.opacity = 0
        self.ids.BoardReworkBtn.disabled = True
        self.ids.BGAReworkBtn.disabled = True

        if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.REWORK_USERS:
            self.ids.BoardReworkBtn.opacity = 1
            self.ids.BoardReworkBtn.disabled = False
            if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.BGA_USERS:
                self.ids.BGAReworkBtn.opacity = 1
                self.ids.BGAReworkBtn.disabled = False
        else:
            self.ids.NoAccessMsg.opacity = 1


    def findBoard(self):
        conn = sqlite3.connect('KioskDB.db')
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT * FROM checkins
                       ORDER BY priority ASC, time_stamp ASC
                       LIMIT 1
                    """)
        result = cursor.fetchone()
        GlobalScreenManager.BOARD_CHECKOUT = str(result)

        print("Top Priority task: (CheckOutScreen) ",result)

        conn.close()

        MDApp.get_running_app().switchScreen('checkOutComfirm')
