#################################################################################
#
#       - File: BRK_CheckInConfirm.py
#       - Author: Dylan Hendrix
#       - Discription: This screen allows the user to confirm their entry
#
################################################################################
#
#       - Entry:   BRK_CheckInBoard.py
#
#       - Exit:    BRK_CloseDoor.py
#
#################################################################################

import pymssql
import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from datetime import datetime

from BRK_GSM import GlobalScreenManager


class CheckInConfirmScreen(Screen):
    def on_enter(self):
        # Populate text fileds
        outputUser = GlobalScreenManager.CURRENT_USER + "  ---  " + GlobalScreenManager.USER_NAMES[GlobalScreenManager.CURRENT_USER]
        self.ids.checkInConfirmUNum.text = str(outputUser)
        self.ids.checkInConfirmMONum.text = str(GlobalScreenManager.CURRENT_MO)
        self.ids.checkInConfirmBoardID.text = str(GlobalScreenManager.CURRENT_BID)
        self.ids.checkInConfirmPriority.text = str(GlobalScreenManager.CURRENT_PRIORITY)
        self.ids.checkInConfirmRWType.text = str(GlobalScreenManager.CURRENT_RW_TYPE)

        # Reset state
        self.ids.completedCheck.opacity = 0
        self.ids.inProgressCheck.opacity = 0
        self.ids.confirmBtn.disabled = True
        self.selected_status = None  # can be "Completed", "In Progress", or None


    def assignStatusCompleted(self):
        if self.selected_status == "Completed": # Second Click
            self.ids.completedCheck.opacity = 0
            self.selected_status = None
            GlobalScreenManager.CURRENT_RW_STATUS = None
            self.ids.confirmBtn.disabled = True
            self.ids.confirmHintTxt.opacity = 1
        else: # First Click
            self.ids.completedCheck.opacity = 1
            self.ids.inProgressCheck.opacity = 0
            self.selected_status = "Completed"
            GlobalScreenManager.CURRENT_RW_STATUS = "Completed"
            self.ids.confirmBtn.disabled = False
            self.ids.confirmHintTxt.opacity = 0


    def assignStatusInProgress(self):
        if self.selected_status == "In Progress": # Second Click
            self.ids.inProgressCheck.opacity = 0
            self.selected_status = None
            GlobalScreenManager.CURRENT_RW_STATUS = None
            self.ids.confirmBtn.disabled = True
            self.ids.confirmHintTxt.opacity = 1
        else: # First Click
            self.ids.inProgressCheck.opacity = 1
            self.ids.completedCheck.opacity = 0
            self.selected_status = "In Progress"
            GlobalScreenManager.CURRENT_RW_STATUS = "In Progress"
            self.ids.confirmBtn.disabled = False
            self.ids.confirmHintTxt.opacity = 0


#################################################################################
#        - Log data after user clicks "Confirm"
#################################################################################
    def assignBox(self):
        # Generate hash Key
        now = datetime.now()
        GlobalScreenManager.HASH_KEY = str(GlobalScreenManager.CURRENT_MO + GlobalScreenManager.CURRENT_BID + now.strftime("%H%M%S"))
        # print(GlobalScreenManager.HASH_KEY)

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
            print("Error assigning kiosk box:",e)

        finally:
            print("KIOSK_BOXES =======================================")
            print("Row[0]: ", GlobalScreenManager.KIOSK_BOXES[0])
            print("Row[1]: ", GlobalScreenManager.KIOSK_BOXES[1])
            print("Row[2]: ", GlobalScreenManager.KIOSK_BOXES[2])

#################################################################################
#        - Push to Kiosk_Table
#################################################################################
        with open("BRK_Creds.json") as f:
            config = json.load(f)

        with pymssql.connect(
            server=config["SERVER"],
            user=config["USER"],
            password=config["PASSWORD"], 
            database=config["DATABASE"]
            ) as conn:
            
            print("Created connection...")
            with conn.cursor() as cursor:
                print("Successfully connected to SQL database.")
                cursor.execute('''
                    INSERT INTO Kiosk_Table (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status, index_row, index_col, rework_type, rework_status)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''', 
                    (
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
                print("Kiosk_Table =====================================")
                cursor.execute('SELECT * FROM Kiosk_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

#################################################################################
#        - Push to Rework_Table
#################################################################################
                cursor.execute('''
                    INSERT INTO Rework_Table (hash_key, [u-num], mo, board_id, priority, time_stamp, in_out_status, rework_type, rework_status)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',
                    (
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
                conn.commit()

            # Print Database
                print("Rework_Table =====================================")
                cursor.execute('SELECT * FROM Rework_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

#################################################################################
#        - Go to Door Screen
#################################################################################
        MDApp.get_running_app().switchScreen('closeDoor')