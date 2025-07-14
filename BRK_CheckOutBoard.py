from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.label import MDLabel

from BRK_GSM import GlobalScreenManager
import sqlite3

class CheckOutBoard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = MDApp.get_running_app().root

    def on_enter(self):
        self.ids.BoardReworkBtn.opacity = 0
        self.ids.BGAReworkBtn.opacity = 0
        self.ids.errorMSG.opacity = 0
        self.ids.BoardReworkBtn.disabled = True
        self.ids.BGAReworkBtn.disabled = True

#################################################################################
#        - Show checkout options based on permissions
#################################################################################
        if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.REWORK_USERS:
            self.ids.BoardReworkBtn.opacity = 1
            self.ids.BoardReworkBtn.disabled = False
            if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.BGA_USERS:
                self.ids.BGAReworkBtn.opacity = 1
                self.ids.BGAReworkBtn.disabled = False
        else:
            self.ids.errorMSG.text = "You are not registered for Check-Out"
            self.ids.errorMSG.opacity = 1

#################################################################################
#        - Search database for next board if any
#################################################################################
    def findBoard(self):
        try:
            conn = sqlite3.connect('KioskDB.db')
            cursor = conn.cursor()

            cursor.execute("""
                        SELECT * FROM checkins
                        ORDER BY priority ASC, time_stamp ASC
                        LIMIT 1
                        """)
            result = cursor.fetchone()

            # Check that database is not empty
            if result is None:
                raise ValueError("No board found")

            GlobalScreenManager.BOARD_CHECKOUT = str(result)
            print("Top Priority task: (CheckOutScreen) ",result)

            MDApp.get_running_app().switchScreen('checkOutConfirm')

        except Exception as e:
            print("No Board in Kiosk")
            print(e)

            self.ids.errorMSG.text = "No Boards in Kiosk"
            self.ids.errorMSG.opacity = 1

            self.ids.BoardReworkBtn.opacity = 0
            self.ids.BGAReworkBtn.opacity = 0
            self.ids.BoardReworkBtn.disabled = True
            self.ids.BGAReworkBtn.disabled = True

            Clock.schedule_once(self.setExceptionText, 2)
            Clock.schedule_once(lambda dt: MDApp.get_running_app().switchScreen('startScreen'), 2.1)

        finally:
            conn.close()


    def setExceptionText(self, dt):
        pass