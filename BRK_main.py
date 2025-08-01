#################################################################################
#
#       - File: BRK_main.py
#       - Author: Dylan Hendrix
#       - Discription: Main file to control the flow of the app, import
#                       screens, and populate inital values
#
################################################################################
#
#       - Entry:   None
#
#       - Exit:    BRK_StartScreen.py
#
#################################################################################

import pymssql
import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import NoTransition,FadeTransition

# Load the format file
from kivy.lang import Builder
Builder.load_file("BRK_Format.kv")

# Import all screens
from BRK_GSM import GlobalScreenManager
from BRK_StartScreen import StartScreen
from BRK_InOutScreen import InOutScreen
from BRK_CheckInBoard import CheckInBoard
from BRK_CheckOutBoard import CheckOutBoard
from BRK_CheckInConfirm import CheckInConfirmScreen
from BRK_CheckOutConfirm import CheckOutConfirm
from BRK_CloseDoor import CloseDoor
from BRK_ListCheckout import ListCheckout
from BRK_AdminConfirm import AdminConfirm
from BRK_AdminEnterUser import AdminEnterUser
from BRK_NoBoardScreen import NoBoardScreen
from BRK_SelectCheckout import SelectCheckout


class BRKGui(MDApp):
    def build(self):
        self.sm = GlobalScreenManager()
        self.sm.add_widget(StartScreen(name='startScreen'))
        self.sm.add_widget(InOutScreen(name='inOutScreen'))
        self.sm.add_widget(CheckInBoard(name='checkInBoard'))
        self.sm.add_widget(CheckOutBoard(name='checkOutBoard'))
        self.sm.add_widget(CheckInConfirmScreen(name='checkInConfirm'))
        self.sm.add_widget(CheckOutConfirm(name='checkOutConfirm'))
        self.sm.add_widget(CloseDoor(name="closeDoor"))
        self.sm.add_widget(ListCheckout(name="listCheckout"))
        self.sm.add_widget(AdminConfirm(name="adminConfirm"))
        self.sm.add_widget(AdminEnterUser(name="adminEnterUser"))
        self.sm.add_widget(NoBoardScreen(name="noBoardScreen"))
        self.sm.add_widget(SelectCheckout(name="selectCheckout"))

        self.populateDoorsList()
        self.populateUsersList()

        self.sm.transition = FadeTransition(duration=0.2) #NoTransition()
        self.theme_cls.theme_style = 'Dark'
        self.switchScreen('startScreen')

        return self.sm

#################################################################################
#        - Init helpers
#################################################################################
    def populateDoorsList(self):
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
                    cursor.execute("SELECT * FROM Kiosk_Table")
                    rows = cursor.fetchall()

                    numRows = len(GlobalScreenManager.KIOSK_BOXES)
                    numCols = len(GlobalScreenManager.KIOSK_BOXES[0]) if numRows > 0 else 0
                    index = 0

                    for row in rows:
                        if index >= numRows * numCols:
                            print("Too many entires in DB. No slots left")
                        else:
                            index_row = int(row[8])
                            index_col = int(row[9])
                            hashKey = row[1]

                            # values[8 and 9] are the index of the slot the physical board is in
                            GlobalScreenManager.KIOSK_BOXES[index_row][index_col] = hashKey
                            index += 1

                except Exception as e:
                    print("Error repopulating kiosk boxes:",e)

                finally:
                    print("KIOSK_BOXES =======================================")
                    print("Row[0]: ", GlobalScreenManager.KIOSK_BOXES[0])
                    print("Row[1]: ", GlobalScreenManager.KIOSK_BOXES[1])
                    print("Row[2]: ", GlobalScreenManager.KIOSK_BOXES[2])

#################################################################################
#        - Pull Users from User Database
#################################################################################
    def populateUsersList(self):
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

                query = "SELECT * FROM User_Table"
                cursor.execute(query)

                data = cursor.fetchall()

                for row in data:
                    GlobalScreenManager.USER_NAMES[row[0]] = row[1]  # Save Usernames with U-Num as the key

                    if row[2] == True: # Basic Access
                        GlobalScreenManager.USERS.append(row[0])
                    if row[3] == True: # Rework Access
                        GlobalScreenManager.REWORK_USERS.append(row[0])
                    if row[4] == True: # BGA Access
                        GlobalScreenManager.BGA_USERS.append(row[0])
                    if row[5] == True: # Admin Access
                        GlobalScreenManager.ADMIN_USERS.append(row[0])
                    if row[6] == True: # Admin Access
                        GlobalScreenManager.QA_USERS.append(row[0])

            # Uncomment to show users pulled from User_Table
                #     print(row)
                # print("REMOTE_DB =============================================================================")
                # print("Users:        ",GlobalScreenManager.USERS)
                # print("Rework Users: ",GlobalScreenManager.REWORK_USERS)
                # print("BGA Users:    ",GlobalScreenManager.BGA_USERS)
                # print("Admin Users:  ",GlobalScreenManager.ADMIN_USERS)
                # print("QA Users:     ",GlobalScreenManager.QA_USERS)
                # print("=======================================================================================")

#################################################################################
#        - Screen functionality
#################################################################################
    def switchScreen(self, newScreen):
        GlobalScreenManager.SCREEN_HIST.append(self.sm.current)
        self.sm.current = newScreen

    def backButton(self, *args):
        if GlobalScreenManager.SCREEN_HIST:
            self.sm.current = GlobalScreenManager.SCREEN_HIST.pop()

#################################################################################
#        - Clean up between cycles
#################################################################################
    def reset(self,dt):
        GlobalScreenManager.CURRENT_USER = 0
        GlobalScreenManager.CURRENT_MO = 0
        GlobalScreenManager.CURRENT_BID = 0
        GlobalScreenManager.CURRENT_PRIORITY = 0
        GlobalScreenManager.CURRENT_RW_TYPE = 0
        GlobalScreenManager.HASH_KEY = 0
        GlobalScreenManager.BOARD_CHECKOUT = 0
        GlobalScreenManager.CURRENT_POS_X = 0
        GlobalScreenManager.CURRENT_POS_Y = 0
        GlobalScreenManager.CHECKOUT_USER = 0
        GlobalScreenManager.CURRENT_RW_STATUS = 0

        self.sm.get_screen('startScreen').ids.EmpID.text = ""

        GlobalScreenManager.SCREEN_HIST.clear()


if __name__ == '__main__':
    BRKGui().run()
