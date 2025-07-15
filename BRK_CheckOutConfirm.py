from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
from BRK_GSM import GlobalScreenManager
import sqlite3


class CheckOutConfirm(Screen):
    def on_enter(self):
        print("==========================================")
        print("Top Priority task: (CheckOutConfirm) ",GlobalScreenManager.BOARD_CHECKOUT)

        Clock.schedule_once(self.delayedInit,0.1)

    def delayedInit(self, dt):
        data = GlobalScreenManager.BOARD_CHECKOUT  # this is already a tuple

        print("SELECTED BOARD:", data)

        self.ids.checkOutConfirmUNum.text = str(GlobalScreenManager.CURRENT_USER)
        self.ids.checkOutConfirmMONum.text = str(data[3])       # MO
        self.ids.checkOutConfirmBoardID.text = str(data[4])     # Board Number
        self.ids.checkOutConfirmPriority.text = str(data[5])    # Priority
        self.ids.checkOutConfirmRWType.text = str(data[10])     # Rework Type

        self.hashKey = str(data[1])

    def confirmCheckOut(self):
        now = datetime.now()
        data = GlobalScreenManager.BOARD_CHECKOUT

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
                in_out_status TEXT,
                rework_type TEXT                              
            )
        ''')

        cursor.execute('''
            INSERT INTO checkins (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status, rework_type)
            values (?,?,?,?,?,?,?,?)
            ''', (   
                data[1], # hash_key
                GlobalScreenManager.CURRENT_USER, # U-Number
                data[3], # MO Number
                data[4], # Board ID
                data[5], # Priority
                now.strftime("%m-%d-%Y %H:%M:%S"),
                "OUT",
                data[10]
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
                    """, (data[1],))

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
                    if GlobalScreenManager.KIOSK_BOXES[i][j] == data[1]:
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
        MDApp.get_running_app().switchScreen('closeDoor')
