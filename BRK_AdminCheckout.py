#################################################################################
#
#       - File: BRK_AdminCheckout.py
#       - Author: Dylan Hendrix
#       - Discription: This screen controls the logic when the user selects
#                       admin checkout from the checkout screen.
#
################################################################################
#
#       - Entry:   BRK_CheckoutBoard.py
#
#       - Exits:   BRK_AdminConfirm.py
#                  BRK_NoBoardScreen.py
#
#################################################################################

import pymssql
import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineListItem

from BRK_GSM import GlobalScreenManager


class AdminCheckout(Screen):
    def on_enter(self):
        self.sortOption("Priority")


    def open_menu(self, item):
        sortOps = ["Priority", "Time", "Board"]
        menu_items = [
            {
                "text": i,
                "on_release": lambda x=i: self.sortOption(x),
            } for i in sortOps
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()


    def sortOption(self, text_item):
        key_map = {
            "Priority": "priority",
            "Time": "time_stamp",
            "Board": "board_id"
        }

        sort_key = key_map.get(text_item, "Priority")
        
        # Refresh the list
        report_list = self.ids.reportList
        report_list.clear_widgets()

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
                    cursor.execute(f"""
                        SELECT * FROM Kiosk_Table
                        ORDER BY {sort_key} ASC
                    """)

                    rows = cursor.fetchall()

                    # Check if kiosk is empty
                    if not rows:
                        print("Database is empty")
                        GlobalScreenManager.noBoardsFlag = "NONE"
                        MDApp.get_running_app().switchScreen("noBoardScreen")

                    for row in rows:
                        item = ThreeLineListItem(
                            text="Board: " + str(row[4]), # Board Number
                            secondary_text="Priority: " + str(row[5]) + " - " + str(row[10]), # Priority
                            tertiary_text="Time: " + str(row[6]), # Entry Time
                            on_release=self.make_select_handler(row)
                        )
                        report_list.add_widget(item)

                    print(f"Sorted by: {sort_key}")

                except Exception as e:
                    print("Error sorting reports:", e)


    def make_select_handler(self, row_data):
        return lambda *args: self.selectReport(row_data)


    def selectReport(self, row):
        GlobalScreenManager.BOARD_CHECKOUT = row
        print("Selected board data:", row)

        MDApp.get_running_app().switchScreen("adminConfirm")