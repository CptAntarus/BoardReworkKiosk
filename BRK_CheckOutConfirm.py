from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from BRK_GSM import GlobalScreenManager, GSM
import sqlite3
import re

class CheckOutConfirm(Screen):
    def on_enter(self):
        print("==========================================")
        print("Top Priority task: (CheckOutConfirm) ",GlobalScreenManager.BOARD_CHECKOUT)

        Clock.schedule_once(self.delayedInit,0.1)

    def delayedInit(self, dt):
        data = GlobalScreenManager.BOARD_CHECKOUT
        pattern = r"(?:'([^']*)'|(\d+))"

        matches = re.findall(pattern, data)
        values = [group[0] if group[0] else group[1] for group in matches]

        print(values)

        self.ids.checkOutConfirmUNum.text = str(GlobalScreenManager.CURRENT_USER)
        self.ids.checkOutConfirmMONum.text = values[3]
        self.ids.checkOutConfirmBoardID.text = values[4]
        self.ids.checkOutConfirmPriority.text = values[5]
        self.hashKey = values[1]

    def confirmCheckOut(self):
        # Remove from slot-list

        # Delete from SQL
        conn = sqlite3.connect('BoardKioskDB.db')
        cursor = conn.cursor()

         # Print Database
        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)

        cursor.execute("""
                       DELETE FROM checkins
                       WHERE hash_key = ?
                    """, (self.hashKey,))
        
        conn.commit()
         # Print Database
        print("\n=======================================\n")
        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)
        
        conn.close()

        # Return to Login
        MDApp.get_running_app().reset(0.1)
        MDApp.get_running_app().switchScreen('startScreen')