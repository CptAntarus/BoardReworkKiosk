#################################################################################
#
#       - File: BRK_ListCheckout.py
#       - Author: Dylan Hendrix
#       - Discription: This screen dynamically displayes the boards to be
#                       checked out based on the type of checkout. The boards
#                       are displayed in a list based on different sort options.
#
################################################################################
#
#       - Comes From:   BRK_SelectCheckout.py
#
#       - Goes To:      BRK_CheckOutConfirm.py
#                       BRK_AdminConfirm.py
#                       BRK_NoBoardScreen.py
#
#################################################################################

import pymssql
import json
import re
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineListItem

from BRK_GSM import GlobalScreenManager


class ListCheckout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = []
        self.DropDownOptions = []

        # Set up dropdown options
        self.AdminOptions = [
            {"text": "Priority", "on_release": lambda x="Priority": self.sortOption(x)},
            {"text": "Time", "on_release": lambda x="Time": self.sortOption(x)},
            {"text": "User", "on_release": lambda: self.whichUserSort()},
        ]
        self.OtherUserOptions = [
            {"text": "Priority", "on_release": lambda x="Priority": self.sortOption(x)},
            {"text": "Time", "on_release": lambda x="Time": self.sortOption(x)},
        ]


    def on_enter(self):
        with open("BRK_Creds.json") as f:
            config = json.load(f)

        with pymssql.connect(
            server=config["SERVER"],
            user=config["USER"],
            password=config["PASSWORD"], 
            database=config["DATABASE"]
            ) as conn:

            print("Creating connection...")
            with conn.cursor() as cursor:
                print("Successfully connected to SQL database.")

                try:
                    if GlobalScreenManager.CHECKOUT_FLAG == "Admin_Checkout":
                        self.DropDownOptions = self.AdminOptions
                        self.ids.ListCheckoutTopBar.title = "Admin Checkout"
                        dataBaseErrorMsg = "Admin Checkout"
                        self.confirmScreen = "adminConfirm"

                        cursor.execute(f"""
                            SELECT * FROM Kiosk_Table
                        """)

                    elif GlobalScreenManager.CHECKOUT_FLAG == "QA_Checkout":
                        self.DropDownOptions = self.OtherUserOptions
                        self.ids.ListCheckoutTopBar.title = "QA Checkout"
                        dataBaseErrorMsg = "QA Checkout"
                        self.confirmScreen = "checkOutConfirm"

                        cursor.execute("""
                            SELECT * FROM Kiosk_Table
                            WHERE rework_status = %s
                            ORDER BY priority DESC
                            """, ("WQA",)) 
            
                    elif GlobalScreenManager.CHECKOUT_FLAG == "IP_Checkout":
                        self.DropDownOptions = self.OtherUserOptions
                        self.ids.ListCheckoutTopBar.title = "Boards You have in Dry Box"
                        dataBaseErrorMsg = "In Progress Checkout"
                        self.confirmScreen = "checkOutConfirm"

                        cursor.execute("""
                            SELECT * FROM Kiosk_Table
                            WHERE (rework_status = %s OR rework_status = %s) AND u_num = %s
                            """, ("In Progress", "Failed QA", GlobalScreenManager.CURRENT_USER))
                    
                    elif GlobalScreenManager.CHECKOUT_FLAG == "Completed_Checkout":
                        self.DropDownOptions = self.OtherUserOptions
                        self.ids.ListCheckoutTopBar.title = "Completed Checkout"
                        dataBaseErrorMsg = "Completed Checkout"
                        self.confirmScreen = "checkOutConfirm"

                        cursor.execute("""
                            SELECT * FROM Kiosk_Table
                            WHERE rework_status = %s
                            """, ("Passed QA",))

                    self.rows = cursor.fetchall()

                    # Check if kiosk is empty
                    if not self.rows:
                        print(f"{dataBaseErrorMsg} is empty")
                        GlobalScreenManager.noBoardsFlag = "NONE"
                        MDApp.get_running_app().switchScreen("noBoardScreen")

                except Exception as e:
                    print("Error getting reports:", e)

                finally:
                    self.sortOption("Priority")


#################################################################################
#        - Drop-down menu builders
#################################################################################
    def open_menu(self, item):
        self.caller = item
        self.mainMenu = MDDropdownMenu(caller=self.caller, items=self.DropDownOptions)
        self.mainMenu.open()


    def whichUserSort(self):
        self.mainMenu.dismiss()
        UsersInKiosk = {row[2] for row in self.rows} # Pull list of Users w/ board(s) in kiosk
        
        # pair uNum with name
        uNumWithName = [
            (uNum, GlobalScreenManager.USER_NAMES[uNum])
            for uNum in UsersInKiosk
        ]

        # Sort by Name
        sortedPairs = sorted(uNumWithName, key=lambda x: x[1].lower())
        
        usersMenuItems = [
            {
                "text": f"{uNum} -- {UserName}", "on_release": lambda x=uNum: self.sortByUser(x)
            } for uNum, UserName in sortedPairs
        ]

        self.userMenu = MDDropdownMenu(caller=self.caller, items=usersMenuItems)
        self.userMenu.open()
    

#################################################################################
#        - Helpers
#################################################################################
    def getTimeDelta(self, row):
        today = datetime.now()
        
        pattern = r"(\d{2})-(\d{2})"
        match = re.match(pattern, row[6])
        if not match:
            return 0
        
        month, day = int(match[1]), int(match[2])

        savedDate = datetime(today.year, month, day)

        if savedDate > today:
            savedDate(today.year - 1, month, day)

        delta = today - savedDate
    
        return delta.days
    

    def convertTimeDeltaToMsg(self, timeDelta):
        if timeDelta == 0:
            timeMsg = "Less than 1 Day"
        elif timeDelta == 1:
            timeMsg = "1 Day"
        elif timeDelta == 2:
            timeMsg = "2 Days"
        elif timeDelta == 3:
            timeMsg = "3 Days"
        elif timeDelta == 4:
            timeMsg = "4 Days"
        elif timeDelta == 5:
            timeMsg = "5 Days"
        elif timeDelta == 6:
            timeMsg = "6 Days"
        elif timeDelta == 7:
            timeMsg = "7 Days"
        elif timeDelta > 7 and timeDelta <= 30:
            timeMsg = "More than a week"
        elif timeDelta > 30:
            timeMsg = "More than 30 Days"

        return timeMsg


#################################################################################
#        - Clear and sort by new option
#################################################################################
    def sortByUser(self, user):
        report_list = self.ids.reportList
        report_list.clear_widgets()

        sortedRows = sorted(self.rows, key=self.getTimeDelta)

        for row in sortedRows:
            ####### Assign time msg #######
            timeDelta = self.getTimeDelta(row)
            timeMsg = self.convertTimeDeltaToMsg(timeDelta)
            if row[11] == "Failed QA":
                addedText = "   * Failed QA *"
            else:
                addedText = ""

            if user == row[2]:
                ####### Make a line in list #######
                item = ThreeLineListItem(
                    text="Board: " + str(row[4]) + f"{addedText}", # Board Number
                    secondary_text="Priority: " + str(row[5]) + " - " + str(row[10]), # Priority & RW Type
                    tertiary_text="Time: " + str(timeMsg), # How long board has been in Kiosk
                    on_release= lambda x, r=row: self.selectReport(r)
                )
                report_list.add_widget(item)


    def sortOption(self, text_item):
        key_map = {
            "Priority": 5,
            "User"    : 2,
            "Time"    : "time"
        }

        sort_key = key_map.get(text_item, "Priority")
        
        # Refresh the list
        report_list = self.ids.reportList
        report_list.clear_widgets()

        if sort_key == "time":
            sortedRows = sorted(self.rows, key=self.getTimeDelta, reverse=True)
        else:
            sortedRows = sorted(self.rows, key=lambda row: row[sort_key])

        for row in sortedRows:
            ####### Assign time msg #######
            timeDelta = self.getTimeDelta(row)
            timeMsg = self.convertTimeDeltaToMsg(timeDelta)
            if row[11] == "Failed QA":
                addedText = "   * Failed QA *"
            else:
                addedText = ""

            ####### Make a line in list #######
            item = ThreeLineListItem(
                text="Board: " + str(row[4]) + f"{addedText}", # Board Number
                secondary_text="Priority: " + str(row[5]) + " - " + str(row[10]), # Priority
                tertiary_text="Time: " + str(timeMsg), # How long board has been in Kiosk
                on_release=lambda x, r=row: self.selectReport(r)
            )
            report_list.add_widget(item)


#################################################################################
#        - Select report and switch screen
#################################################################################
    def selectReport(self, row):
        GlobalScreenManager.CHECKOUT_USER = GlobalScreenManager.CURRENT_USER
        GlobalScreenManager.BOARD_CHECKOUT = row
        # print("Selected board data:", row)

        MDApp.get_running_app().switchScreen(f"{self.confirmScreen}")
