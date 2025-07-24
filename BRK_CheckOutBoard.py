#################################################################################
#
#       - File: BRK_CheckOutBoard.py
#       - Author: Dylan Hendrix
#       - Discription: This screen controls the initial checkout process
#                       and passes control to the different checkout
#                       methods.
#
################################################################################
#
#       - Entry:   BRK_InOutScreen.py
#
#       - Exits:   BRK_CheckOutConfirm.py
#                  BRK_AdminCheckout.py
#                  BRK_NoBoardScreen.py
#
#################################################################################

import pymssql
import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager


class CheckOutBoard(Screen):
    def on_enter(self):
        # Disable all buttons before permissions validation
        self.ids.BoardReworkBtn.opacity = 0
        self.ids.BGAReworkBtn.opacity = 0
        self.ids.AdminCheckoutBtn.opacity = 0
        self.ids.AdminCheckoutBtn.disabled = True
        self.ids.BoardReworkBtn.disabled = True
        self.ids.BGAReworkBtn.disabled = True

#################################################################################
#        - Show checkout options based on permissions
#################################################################################
        if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.REWORK_USERS:
            self.ids.checkOutLabel.opacity = 1
            self.ids.BoardReworkBtn.opacity = 1
            self.ids.BoardReworkBtn.disabled = False
            if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.BGA_USERS:
                self.ids.BGAReworkBtn.opacity = 1
                self.ids.BGAReworkBtn.disabled = False
                if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.ADMIN_USERS:
                    self.ids.AdminCheckoutBtn.opacity = 1
                    self.ids.AdminCheckoutBtn.disabled = False
        else:
            self.ids.errorMSG.text = "You are not registered for Check-Out"
            self.ids.checkOutLabel.opacity = 0
            self.ids.errorMSG.opacity = 1


#################################################################################
#        - Search Kiosk_Table for next Normal board rework if any
#################################################################################
    def findNBRBoard(self):
        try:
            with open("BRK_Creds.json") as f:
                config = json.load(f)

            with pymssql.connect(
                server=config["SERVER"],
                user=config["USER"],
                password=config["PASSWORD"], 
                database=config["DATABASE"]
                ) as conn:

                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT TOP 1 * FROM Kiosk_Table
                        WHERE rework_type = 'NBR'
                        ORDER BY priority ASC, time_stamp ASC
                    """)
                    result = cursor.fetchone()

            # Check that Kiosk_Table is not empty
            if result is None:
                raise ValueError("No board found")

            GlobalScreenManager.BOARD_CHECKOUT = result
            GlobalScreenManager.CHECKOUT_USER = GlobalScreenManager.CURRENT_USER
            print("Top Priority task: ",result)

            MDApp.get_running_app().switchScreen('checkOutConfirm')

        except Exception as e:
            print(e)

            GlobalScreenManager.noBoardsFlag = 'NBR'
            MDApp.get_running_app().switchScreen('noBoardScreen')


#################################################################################
#        - Search Kiosk_Table for next BGA rework if any
#################################################################################
    def findBGABoard(self):
        try:
            with open("BRK_Creds.json") as f:
                config = json.load(f)

            with pymssql.connect(
                server=config["SERVER"],
                user=config["USER"],
                password=config["PASSWORD"], 
                database=config["DATABASE"]
                ) as conn:

                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT TOP 1 * FROM Kiosk_Table
                        WHERE rework_type = 'BGA'
                        ORDER BY priority ASC, time_stamp ASC
                    """)
                    result = cursor.fetchone()

            # Check that Kiosk_Table is not empty
            if result is None:
                raise ValueError("No board found")

            GlobalScreenManager.BOARD_CHECKOUT = result
            GlobalScreenManager.CHECKOUT_USER = GlobalScreenManager.CURRENT_USER
            print("Top Priority task: ",result)

            MDApp.get_running_app().switchScreen('checkOutConfirm')

        except Exception as e:
            print(e)

            GlobalScreenManager.noBoardsFlag = 'BGA'
            MDApp.get_running_app().switchScreen('noBoardScreen')
