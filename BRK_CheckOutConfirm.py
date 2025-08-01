#################################################################################
#
#       - File: BRK_CheckOutConfirm.py
#       - Author: Dylan Hendrix
#       - Discription: This screen allows the user to confirm their checkout
#
################################################################################
#
#       - Entry:   BRK_CheckoutBoard.py
#
#       - Exit:    BRK_CloseDoor.py
#
#################################################################################

import pymssql
import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime

from BRK_GSM import GlobalScreenManager


class CheckOutConfirm(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.newStatus = ""


    def on_enter(self):
        Clock.schedule_once(self.delayedInit,0.1)


    def delayedInit(self, dt):
        # Board being checked out from Kiosk_Table
        data = GlobalScreenManager.BOARD_CHECKOUT

        print("==========================================")
        print("SELECTED BOARD:", data)

        # Populate text fileds
        outputUser = str(GlobalScreenManager.CHECKOUT_USER) + "  ---  " + str(GlobalScreenManager.USER_NAMES[GlobalScreenManager.CHECKOUT_USER])
        self.ids.checkOutConfirmUNum.text = str(outputUser)     # U-num & Name
        self.ids.checkOutConfirmMONum.text = str(data[3])       # MO
        self.ids.checkOutConfirmBoardID.text = str(data[4])     # Board Number
        self.ids.checkOutConfirmPriority.text = str(data[5])    # Priority
        self.ids.checkOutConfirmRWType.text = str(data[10])     # Rework Type

        self.hashKey = str(data[1])

        # Handle Status logic
        if data[11] == "Initial":
            self.newStatus = "In Progress"
        elif data[11] == "In Progress":
            self.newStatus = "In Progress"
        elif data[11] == "WQA":
            self.newStatus = "In QA"
        elif data[11] == "Failed QA":
            self.newStatus = "Failed QA"
        elif data[11] == "Passed QA":
            self.newStatus = "Passed QA"


        print("data[11]: ", data[11])
        print("Status: ", self.newStatus)


    def confirmCheckOut(self):
        # Save current time & board being checked out
        self.now = datetime.now()
        data = GlobalScreenManager.BOARD_CHECKOUT
    
        if data[11] == "Passed QA":
            print("Doing completed branch")
            self.completedCheckout()
            return

#################################################################################
#        - Copy over to Rework_Table
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
                    INSERT INTO Rework_Table (hash_key, [u-num], mo, board_id, priority, time_stamp, in_out_status, rework_type, rework_status)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',
                    (
                        data[1],  # hash_key
                        GlobalScreenManager.CHECKOUT_USER, # U-Number
                        data[3],  # MO Number
                        data[4],  # Board ID
                        data[5],  # Priority
                        self.now.strftime("%m-%d-%Y %H:%M:%S"), # Time
                        "OUT",    # Operation
                        data[10], # rework_type
                        self.newStatus  # rework_status
                    )
                )
                conn.commit()

            # Print Database (Can be removed for final product)
                print("Rework_Table =====================================")
                cursor.execute('SELECT * FROM Rework_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

#################################################################################
#        - Delete from Kiosk_Table
#################################################################################
                cursor.execute("DELETE FROM Kiosk_Table WHERE hash_key = %s", (data[1],))
                conn.commit()

            # Print Database (Can be removed for final product)
                print("Kiosk_Table =====================================")
                cursor.execute('SELECT * FROM Kiosk_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

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
            print("Error removing board from kiosk boxes:",e)

        finally:
            print("KIOSK_BOXES =======================================")
            print("Row[0]: ", GlobalScreenManager.KIOSK_BOXES[0])
            print("Row[1]: ", GlobalScreenManager.KIOSK_BOXES[1])
            print("Row[2]: ", GlobalScreenManager.KIOSK_BOXES[2])

        MDApp.get_running_app().switchScreen('closeDoor')


#################################################################################
#       - Handle Completed Process
#################################################################################
    def completedCheckout(self):
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
                CompletedBoard = GlobalScreenManager.BOARD_CHECKOUT
                boardID = CompletedBoard[4]

                # Grab all entries of completed board from Rework_Table
                cursor.execute("""
                    SELECT * FROM Rework_Table WHERE board_id = %s      
                """, (boardID,))
                entriesOfCompletedBoard = cursor.fetchall()

                print("THING TO TEST: ", entriesOfCompletedBoard)

                # Push to History Table
                for row in entriesOfCompletedBoard:
                    cursor.execute("""
                        INSERT INTO History_Table (
                            [log count], hash_key, [u-num], mo, board_id, priority, time_stamp, in_out_status, rework_type, rework_status
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (row))
                    conn.commit()

                print("History_Table =====================================")
                cursor.execute('SELECT * FROM History_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

#################################################################################
#       - Remove from Rework_Table
#################################################################################
                cursor.execute("DELETE FROM Rework_Table WHERE board_id = %s", (boardID,))
                conn.commit()

            # Print Database (Can be removed for final product)
                print("Rework_Table =====================================")
                cursor.execute('SELECT * FROM Rework_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

#################################################################################
#       - Remove from KIOSK_BOXES
#################################################################################
                cursor.execute("DELETE FROM Kiosk_Table WHERE board_id = %s", (boardID,))
                conn.commit()

            # Print Database (Can be removed for final product)
                print("Kiosk_Table =====================================")
                cursor.execute('SELECT * FROM Kiosk_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        
        
        MDApp.get_running_app().switchScreen('closeDoor')