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
        self.rows = "Blank"

        # Reset state
        self.deactivateStatusBtns()
        self.ids.BtnOneCheck.opacity = 0
        self.ids.BtnTwoCheck.opacity = 0
        self.ids.confirmBtn.disabled = True
        self.BtnStatus = None

#################################################################################
#        - Pull list of Boards from Kiosk_DB
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

                try:
                    cursor.execute("""
                                   SELECT * FROM Rework_Table
                                   WHERE board_id = %s
                                   ORDER BY time_stamp DESC
                                   """, (GlobalScreenManager.CURRENT_BID,))
                    self.rows = cursor.fetchall()
                except Exception as e:
                    print("Error repopulating kiosk boxes:",e)
                finally:
                     print("Done getting rows")
                     print("self.rows", self.rows)

        # Handle Status logic
        print("CURRENT_BID: ", GlobalScreenManager.CURRENT_BID)
        if not any(row[4] == GlobalScreenManager.CURRENT_BID for row in self.rows):    # New Board
            GlobalScreenManager.CURRENT_RW_STATUS = "Initial"
            self.ids.confirmBtn.disabled = False
            print("Doing the if side")

        elif self.rows[0][9] == "Initial":
            print("ERROR: Board Checked In A second Time without Checkout")
            self.deactivateStatusBtns()
            self.ids.confirmBtn.disabled = False

        else:
            print("Doing the else side")
            selectedBoard = self.rows[0]
            GlobalScreenManager.CURRENT_RW_STATUS = selectedBoard[9]
            self.activateStatusBtns()

            if GlobalScreenManager.CURRENT_RW_STATUS == "In Progress":
                print("something might have worked")
                self.ids.statusBtnOne.text = "In Progress"
                self.status1 = "In Progress"
                self.ids.statusBtnTwo.text = "Waiting For QA"
                self.status2 = "WQA"
            elif GlobalScreenManager.CURRENT_RW_STATUS == "In QA":
                print("something might have worked a second time!")
                self.ids.statusBtnOne.text = "Redo"
                self.status1 = "Redo"
                self.ids.statusBtnTwo.text = "Completed"
                self.status2 = "Completed"

        
            
            #change button text and values

        print("Status: ", GlobalScreenManager.CURRENT_RW_STATUS)

    def activateStatusBtns(self):
        self.ids.statusBtnOne.opacity = 1
        self.ids.statusBtnOne.disabled = False
        self.ids.statusBtnTwo.opacity = 1
        self.ids.statusBtnTwo.disabled = False

    def deactivateStatusBtns(self):
        self.ids.statusBtnOne.opacity = 0
        self.ids.statusBtnOne.disabled = True
        self.ids.statusBtnTwo.opacity = 0
        self.ids.statusBtnTwo.disabled = True


    def assignStatusBtnOne(self, status):
        if self.BtnStatus == status: # Second Click
            self.ids.BtnOneCheck.opacity = 0
            self.BtnStatus = None
            GlobalScreenManager.CURRENT_RW_STATUS = None
            self.ids.confirmBtn.disabled = True
            self.ids.confirmHintTxt.opacity = 1
        else: # First Click
            self.ids.BtnOneCheck.opacity = 1
            self.ids.BtnTwoCheck.opacity = 0
            self.BtnStatus = status
            GlobalScreenManager.CURRENT_RW_STATUS = self.status1
            self.ids.confirmBtn.disabled = False
            self.ids.confirmHintTxt.opacity = 0


    def assignStatusBtnTwo(self, status):
        if self.BtnStatus == status: # Second Click
            self.ids.BtnTwoCheck.opacity = 0
            self.BtnStatus = None
            GlobalScreenManager.CURRENT_RW_STATUS = None
            self.ids.confirmBtn.disabled = True
            self.ids.confirmHintTxt.opacity = 1
        else: # First Click
            self.ids.BtnTwoCheck.opacity = 1
            self.ids.BtnOneCheck.opacity = 0
            self.BtnStatus = status
            GlobalScreenManager.CURRENT_RW_STATUS = self.status2
            self.ids.confirmBtn.disabled = False
            self.ids.confirmHintTxt.opacity = 0


#################################################################################
#        - Log data after user clicks "Confirm"
#################################################################################
    def assignBox(self):
        print("Status: ", GlobalScreenManager.CURRENT_RW_STATUS)

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

################################################################################
#       - Go to Door Screen
################################################################################
        MDApp.get_running_app().switchScreen('closeDoor')