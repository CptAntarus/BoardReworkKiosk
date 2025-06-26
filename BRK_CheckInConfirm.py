from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from datetime import datetime
import sqlite3

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

        # Assign a slot in the kiosk
        assigned = False
        for row in range(len(GlobalScreenManager.KIOSK_BOXES)):
            if assigned:
                break
            for col in range(len(GlobalScreenManager.KIOSK_BOXES[row])):
                if assigned:
                    break
                for slot in range(len(GlobalScreenManager.KIOSK_BOXES[row][col])):
                    if not GlobalScreenManager.KIOSK_BOXES[row][col][slot]:
                        GlobalScreenManager.KIOSK_BOXES[row][col][slot] = GlobalScreenManager.HASH_KEY
                        assigned = True
                        break

        print(GlobalScreenManager.KIOSK_BOXES[row][col][slot])
        print(GlobalScreenManager.KIOSK_BOXES)

        # Push to SQL
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash_key TEXT,
                u_num TEXT,
                mo TEXT,
                board_id TEXT,
                priority TEXT,
                time_stamp TEXT                                
            )
        ''')

        cursor.execute('''
            INSERT INTO checkins (hash_key, u_num, mo, board_id, priority, time_stamp)
            values (?,?,?,?,?,?)
            ''', (
                GlobalScreenManager.HASH_KEY,
                GlobalScreenManager.CURRENT_USER,
                GlobalScreenManager.CURRENT_MO,
                GlobalScreenManager.CURRENT_BID,
                GlobalScreenManager.CURRENT_PRIORITY,
                now.strftime("%m/%d/%Y %H:%M:%S")
            )
        )

        conn.commit()

        for row in cursor.execute('SELECT * FROM checkins'):
            print(row)
            
        conn.close()

        self.manager.current = 'startScreen'
