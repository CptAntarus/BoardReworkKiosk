from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from datetime import datetime
import sqlite3
import re

from BRK_GSM import GlobalScreenManager, GSM

class CheckInConfirmScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = GSM()

    def on_enter(self):
        self.ids.checkInConfirmUNum.text = str(GlobalScreenManager.CURRENT_USER)
        self.ids.checkInConfirmMONum.text = str(GlobalScreenManager.CURRENT_MO)
        self.ids.checkInConfirmBoardID.text = str(GlobalScreenManager.CURRENT_BID)
        self.ids.checkInConfirmPriority.text = str(GlobalScreenManager.CURRENT_PRIORITY)
        self.ids.checkInConfirmRWType.text = str(GlobalScreenManager.CURRENT_RW_TYPE)

        self.ids.completedCheck.opacity = 0
        self.ids.inProgressCheck.opacity = 0
        self.ids.confirmBtn.disabled = True
        self.completed = 0
        self.inProgress = 0

    def assignStatusCompleted(self):
        self.completed = 0 if self.completed else 1
        self.ids.completedCheck.opacity = 1 if self.completed else 0
        self.ids.inProgressCheck.opacity = 0
        self.inProgress = 0
        self.ids.confirmBtn.disabled = False
        GlobalScreenManager.CURRENT_RW_STATUS = "Completed"



    def assignStatusInProgress(self):
        self.inProgress = 0 if self.inProgress else 1
        self.ids.inProgressCheck.opacity = 1 if self.inProgress else 0
        self.ids.completedCheck.opacity = 0
        self.completed = 0
        self.ids.confirmBtn.disabled = False
        GlobalScreenManager.CURRENT_RW_STATUS = "In Progress"

    def assignBox(self):
        # Create hash Key
        now = datetime.now()
        GlobalScreenManager.HASH_KEY = str(GlobalScreenManager.CURRENT_MO + GlobalScreenManager.CURRENT_BID + now.strftime("%H%M%S"))
        print(GlobalScreenManager.HASH_KEY)

#################################################################################
#        - Assign a slot in the kiosk
#################################################################################
        try:            
            numRows = len(GlobalScreenManager.KIOSK_BOXES)
            numCols = len(GlobalScreenManager.KIOSK_BOXES[0]) if numRows > 0 else 0
            assigned = False

            for i in range(numRows):
                for j in range(numCols):
                    if GlobalScreenManager.KIOSK_BOXES[i][j] is None:
                        GlobalScreenManager.KIOSK_BOXES[i][j] = GlobalScreenManager.HASH_KEY
                        self.indexRow = i
                        self.indexCol = j

                        GlobalScreenManager.CURRENT_POS_X = i
                        GlobalScreenManager.CURRENT_POS_Y = j
                        

                        assigned = True
                        break
                if assigned:
                    break

        except Exception as e:
            print("Error repopulating kiosk boxes:",e)

        finally:
            print("KIOSK_BOXES =======================================")
            print(GlobalScreenManager.KIOSK_BOXES)

#################################################################################
#        - Push to KioskDB
#################################################################################
        conn = sqlite3.connect('KioskDB.db')
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
                index_row,
                index_col,
                rework_type TEXT,
                rework_status TEXT
            )
        ''')

        cursor.execute('''
            INSERT INTO checkins (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status, index_row, index_col, rework_type, rework_status)
            values (?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                GlobalScreenManager.HASH_KEY,
                GlobalScreenManager.CURRENT_USER,
                GlobalScreenManager.CURRENT_MO,
                GlobalScreenManager.CURRENT_BID,
                GlobalScreenManager.CURRENT_PRIORITY,
                now.strftime("%m-%d-%Y %H:%M:%S"),
                "IN",
                self.indexRow,
                self.indexCol,
                GlobalScreenManager.CURRENT_RW_TYPE,
                GlobalScreenManager.CURRENT_RW_STATUS
            )
        )

        conn.commit()

        # Print Database
        print("KIOSK_DB =====================================")
        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)
            
        conn.close()

#################################################################################
#        - Push to ReworkDB
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
                rework_type TEXT,
                rework_status TEXT                               
            )
        ''')

        cursor.execute('''
            INSERT INTO checkins (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status, rework_type, rework_status)
            values (?,?,?,?,?,?,?,?,?)
            ''', (
                GlobalScreenManager.HASH_KEY,
                GlobalScreenManager.CURRENT_USER,
                GlobalScreenManager.CURRENT_MO,
                GlobalScreenManager.CURRENT_BID,
                GlobalScreenManager.CURRENT_PRIORITY,
                now.strftime("%m-%d-%Y %H:%M:%S"),
                "IN",
                GlobalScreenManager.CURRENT_RW_TYPE,
                GlobalScreenManager.CURRENT_RW_STATUS
            )
        )

        # Print Database
        print("REWORK_DB =====================================")
        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)
            
        conn.commit()
        conn.close()

#################################################################################
#        - Go to Door Screen
#################################################################################
        MDApp.get_running_app().switchScreen('closeDoor')