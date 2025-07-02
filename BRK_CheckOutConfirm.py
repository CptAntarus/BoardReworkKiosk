from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
from BRK_GSM import GlobalScreenManager
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
        self.values = [group[0] if group[0] else group[1] for group in matches]

        print("SELECTED BOARD: ", self.values)

        self.ids.checkOutConfirmUNum.text = str(GlobalScreenManager.CURRENT_USER)
        self.ids.checkOutConfirmMONum.text = self.values[3]
        self.ids.checkOutConfirmBoardID.text = self.values[4]
        self.ids.checkOutConfirmPriority.text = self.values[5]
        self.hashKey = self.values[1]

    def confirmCheckOut(self):
        now = datetime.now()
        # Remove from KIOSK_BOXES

#################################################################################
#        - Copy over to ReworkDB
#################################################################################
        conn = sqlite3.connect('ReworkDB.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash_key TEXT,
                u_num TEXT,
                mo TEXT,
                board_id TEXT,
                priority TEXT,
                time_stamp TEXT,
                in_out_status TEXT                                
            )
        ''')

        cursor.execute('''
            INSERT INTO checkins (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status)
            values (?,?,?,?,?,?,?)
            ''', (   
                self.values[1],
                self.values[2],
                self.values[3],
                self.values[4],
                self.values[5],
                now.strftime("%m-%d-%Y %H:%M:%S"),
                "OUT"
            )
        )

        # Print Database
        print("ReworkDB =====================================")
        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)

        conn.commit()
        conn.close()

#################################################################################
#        - Delete from KioskDB
#################################################################################
        conn = sqlite3.connect('KioskDB.db')
        cursor = conn.cursor()

        cursor.execute("""
                       DELETE FROM checkins
                       WHERE hash_key = ?
                    """, (self.hashKey,))

         # Print Database
        print("KioskDB =======================================")
        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)
        
        conn.commit()
        conn.close()


#################################################################################
#       - Remove from KIOSK_BOXES
#################################################################################
        try:
            numRows = len(GlobalScreenManager.KIOSK_BOXES)
            numCols = len(GlobalScreenManager.KIOSK_BOXES[0]) if numRows > 0 else 0
            removed = False

            for i in range(numRows):
                for j in range(numCols):
                    if GlobalScreenManager.KIOSK_BOXES[i][j] == self.values[1]:
                        GlobalScreenManager.KIOSK_BOXES[i][j] = None
                        removed = True
                        break
                if removed:
                    break

        except Exception as e:
            print("Error repopulating kiosk boxes:",e)

        finally:
            print("KIOSK_BOXES =======================================")
            print(GlobalScreenManager.KIOSK_BOXES)
            
#################################################################################
#       - Return to Login
#################################################################################
        MDApp.get_running_app().reset(0.1)
        MDApp.get_running_app().switchScreen('startScreen')
