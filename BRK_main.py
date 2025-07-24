import pymssql

# KivyMD Imports
from kivymd.app import MDApp

# Kivy Imports
from kivy.uix.screenmanager import NoTransition

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
from BRK_AdminCheckout import AdminCheckout
from BRK_AdminConfirm import AdminConfirm
from BRK_AdminEnterUser import AdminEnterUser


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
        self.sm.add_widget(AdminCheckout(name="adminCheckout"))
        self.sm.add_widget(AdminConfirm(name="adminConfirm"))
        self.sm.add_widget(AdminEnterUser(name="adminEnterUser"))

        self.populateDoorsList()
        self.populateUsersList()

        self.sm.transition = NoTransition()
        self.theme_cls.theme_style = 'Dark'
        self.switchScreen('startScreen')

        return self.sm

#################################################################################
#        - Init helpers
#################################################################################
    def populateDoorsList(self):
        server='USW-SQL30003.rootforest.com'
        user='OvenBakedUsr'
        password='aztmvcjfrizkcpdcehky'
        database='Oven_Bake_Log'
        with pymssql.connect(server, user, password, database) as conn:
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

                            # print(f"values[8]: {values[8]}:::::::::values[9]: {values[9]}")

                            # values[8 and 9] are the index of the slot the physical board is in
                            GlobalScreenManager.KIOSK_BOXES[index_row][index_col] = hashKey
                            index += 1

                except Exception as e:
                    print("Error repopulating kiosk boxes:",e)

                finally:
                    print(GlobalScreenManager.KIOSK_BOXES)

#################################################################################
#        - Pull Users from User Database
#################################################################################
    def populateUsersList(self):
        server='USW-SQL30003.rootforest.com'
        user='OvenBakedUsr'
        password='aztmvcjfrizkcpdcehky'
        database='Oven_Bake_Log'
        with pymssql.connect(server, user, password, database) as conn:
            print("Created connection...")
            with conn.cursor() as cursor:
                print("Successfully connected to SQL database.")

                query = "SELECT * FROM User_Table"
                cursor.execute(query)

                data = cursor.fetchall()

                for row in data:
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
                    # print(row)
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
        self.sm.get_screen('checkInBoard').ids.boardInMO.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInBarCode.text = ""
        self.sm.get_screen('checkInBoard').ids.boardInPriority.text = ""

        GlobalScreenManager.SCREEN_HIST.clear()

if __name__ == '__main__':
    BRKGui().run()
