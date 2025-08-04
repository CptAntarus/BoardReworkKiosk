#################################################################################
#
#       - File: BRK_CheckInConfirm.py
#       - Author: Dylan Hendrix
#       - Discription: This screen allows the user to confirm their entry
#
#       - Notes:
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
        self.status1 = ""
        self.status2 = ""

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


#################################################################################
#        - Handle Status logic (Check INCOMMING baord)
#################################################################################
        # New Board
        print("CURRENT_BID: ", GlobalScreenManager.CURRENT_BID)
        if not any(row[4] == GlobalScreenManager.CURRENT_BID for row in self.rows):    
            GlobalScreenManager.CURRENT_RW_STATUS = "Initial"
            self.ids.confirmBtn.disabled = False
            print("Doing the if side")

        # If it is in the kiosk but already has 'IN' tag, ie it's already in the dry box
        elif self.rows[0][7] == "IN" or self.rows[0][9] == "DOUBLE":
            print("ERROR: Board Checked In A second Time without Checkout")
            GlobalScreenManager.noBoardsFlag = "DOUBLE"
            MDApp.get_running_app().switchScreen("noBoardScreen")

        # Everything else
        else:
            print("Doing the else side")
            selectedBoard = self.rows[0]
            GlobalScreenManager.CURRENT_RW_STATUS = selectedBoard[9]
            self.activateStatusBtns()

            if GlobalScreenManager.CURRENT_RW_STATUS == "In Progress":
                self.ids.statusBtnOne.text = "In Progress"
                self.status1 = "In Progress"
                self.ids.statusBtnTwo.text = "Waiting For QA"
                self.status2 = "WQA"
            elif GlobalScreenManager.CURRENT_RW_STATUS == "In QA":
                self.ids.statusBtnOne.text = "Failed QA"
                self.status1 = "Failed QA"
                self.ids.statusBtnTwo.text = "Passed QA"
                self.status2 = "Passed QA"
            elif GlobalScreenManager.CURRENT_RW_STATUS == "Failed QA":
                self.ids.statusBtnOne.text = "In Progress"
                self.status1 = "Failed QA" # Keep 'Failed QA' Status
                self.ids.statusBtnTwo.text = "Waiting For QA"
                self.status2 = "WQA"
            elif GlobalScreenManager.CURRENT_RW_STATUS == "Passed QA":
                print("ERROR: Board Checked In A second Time without Checkout")
                GlobalScreenManager.noBoardsFlag = "DONE"
                MDApp.get_running_app().switchScreen("noBoardScreen")


        print("Status: ", GlobalScreenManager.CURRENT_RW_STATUS)


    def activateStatusBtns(self):
        self.ids.confirmHintTxt.opacity = 1
        self.ids.statusBtnOne.opacity = 1
        self.ids.statusBtnOne.disabled = False
        self.ids.statusBtnTwo.opacity = 1
        self.ids.statusBtnTwo.disabled = False

    def deactivateStatusBtns(self):
        self.ids.confirmHintTxt.opacity = 0
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

                print("BEFORE THE IF THING")
                # if redo assign to previous user
                checkinUser = ""
                if GlobalScreenManager.CURRENT_RW_STATUS == "Failed QA":
                    # Find user who submited board for QA
                    cursor.execute("""
                        SELECT * FROM Rework_Table
                        WHERE board_id = %s AND rework_status = %s
                        """, (GlobalScreenManager.CURRENT_BID, "WQA"))
                    self.rows = cursor.fetchone()
                    checkinUser = str(self.rows[2])
                    print(f"IF:checkinUser: {checkinUser}")
                else:
                    checkinUser = GlobalScreenManager.CURRENT_USER
                    print(f"ELSE:checkinUser: {checkinUser}")
                print("AFTER THE IF THING")
                

                # Insert into Kiosk_Table
                cursor.execute('''
                    INSERT INTO Kiosk_Table (hash_key, u_num, mo, board_id, priority, time_stamp, in_out_status, index_row, index_col, rework_type, rework_status)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''', 
                    (
                        GlobalScreenManager.HASH_KEY,
                        checkinUser,
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
                        checkinUser,
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