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


    def assignBox(self):
        # Create hash Key
        now = datetime.now()
        GlobalScreenManager.HASH_KEY = str(GlobalScreenManager.CURRENT_MO + GlobalScreenManager.CURRENT_BID + now.strftime("%H%M%S"))
        print(GlobalScreenManager.HASH_KEY)

#################################################################################
#        - Assign a slot in the kiosk (REWORK LATER)
#################################################################################
        # assigned = False
        # for row in range(len(GlobalScreenManager.KIOSK_BOXES)):
        #     if assigned:
        #         break
        #     for col in range(len(GlobalScreenManager.KIOSK_BOXES[row])):
        #         if assigned:
        #             break
        #         for slot in range(len(GlobalScreenManager.KIOSK_BOXES[row][col])):
        #             if not GlobalScreenManager.KIOSK_BOXES[row][col][slot]:
        #                 GlobalScreenManager.KIOSK_BOXES[row][col][slot] = GlobalScreenManager.HASH_KEY
        #                 assigned = True
        #                 break

        # print(GlobalScreenManager.KIOSK_BOXES[row][col][slot])
        # print(GlobalScreenManager.KIOSK_BOXES)

        try:            
            numRows = len(GlobalScreenManager.KIOSK_BOXES)
            numCols = len(GlobalScreenManager.KIOSK_BOXES[0]) if numRows > 0 else 0
            assigned = False

            for i in range(numRows):
                for j in range(numCols):
                    if GlobalScreenManager.KIOSK_BOXES[i][j] is None:
                        GlobalScreenManager.KIOSK_BOXES[i][j] = GlobalScreenManager.HASH_KEY
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
                in_out_status TEXT                                
            )
        ''')

        cursor.execute('''
            INSERT INTO checkins (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status)
            values (?,?,?,?,?,?,?)
            ''', (
                GlobalScreenManager.HASH_KEY,
                GlobalScreenManager.CURRENT_USER,
                GlobalScreenManager.CURRENT_MO,
                GlobalScreenManager.CURRENT_BID,
                GlobalScreenManager.CURRENT_PRIORITY,
                now.strftime("%m-%d-%Y %H:%M:%S"),
                "IN"
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
                in_out_status TEXT                                
            )
        ''')

        cursor.execute('''
            INSERT INTO checkins (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status)
            values (?,?,?,?,?,?,?)
            ''', (
                GlobalScreenManager.HASH_KEY,
                GlobalScreenManager.CURRENT_USER,
                GlobalScreenManager.CURRENT_MO,
                GlobalScreenManager.CURRENT_BID,
                GlobalScreenManager.CURRENT_PRIORITY,
                now.strftime("%m-%d-%Y %H:%M:%S"),
                "IN"
            )
        )

        # Print Database
        print("REWORK_DB =====================================")
        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)
            
        conn.commit()
        conn.close()

#################################################################################
#        - Return to Login
#################################################################################
        MDApp.get_running_app().reset(.1)
        MDApp.get_running_app().switchScreen('startScreen')