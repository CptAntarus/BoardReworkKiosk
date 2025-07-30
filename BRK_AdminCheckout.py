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
import re
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineListItem

from BRK_GSM import GlobalScreenManager


class AdminCheckout(Screen):
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
                    cursor.execute(f"""
                        SELECT * FROM Kiosk_Table
                    """)
                        # ORDER BY {sort_key} ASC

                    self.rows = cursor.fetchall()

                    # Check if kiosk is empty
                    if not self.rows:
                        print("Database is empty")
                        GlobalScreenManager.noBoardsFlag = "NONE"
                        MDApp.get_running_app().switchScreen("noBoardScreen")

                except Exception as e:
                    print("Error sorting reports:", e)

                finally:
                    self.sortOption("Priority")


#################################################################################
#        - Drop-down menu builders
#################################################################################
    def open_menu(self, item):
        menu_items = [
            {"text": "Priority", "on_release": lambda x="Priority": self.sortOption(x)},
            {"text": "Time", "on_release": lambda x="Time": self.sortOption(x)},
            {"text": "User", "on_release": lambda: self.whichUserSort()},
        ]
        self.caller = item
        self.mainMenu = MDDropdownMenu(caller=self.caller, items=menu_items)
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
        nowMonth = int(datetime.now().strftime("%m"))
        nowDay = int(datetime.now().strftime("%d"))
        nowYear = int(datetime.now().strftime("%Y"))
        # print("+",nowMonth,nowDay,nowYear,"+")

        pattern = r"(\d{2})-(\d{2})"
        longMonths = [1,3,5,7,8,10,11]
        mediumMonths = [4,6,9,11]

        ####### Get Data Time Difference #######
        match = re.match(pattern, row[6])
        parts = match.groups() # parts = [month,day]

        savedMonth = int(parts[0])
        savedDay = int(parts[1])
        deltaDay = nowDay - savedDay

        # Calculte time in Kiosk
        if nowMonth != savedMonth: # board from prev month
            if savedMonth in longMonths:
                timeDelta = (31-savedDay) + nowDay
            if savedMonth in mediumMonths:
                timeDelta = (30-savedDay) + nowDay
            if savedMonth == 2:
                timeDelta = (28-savedDay) + nowDay
        else:
            timeDelta = deltaDay

        return timeDelta
    

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

            if user == row[2]:
                ####### Make a line in list #######
                item = ThreeLineListItem(
                    text="Board: " + str(row[4]), # Board Number
                    secondary_text="Priority: " + str(row[5]) + " - " + str(row[10]), # Priority & RW Type
                    tertiary_text="Time: " + str(timeMsg), # How long board has been in Kiosk
                    on_release= lambda x: self.selectReport(row)
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
            sortedRows = sorted(self.rows, key=self.getTimeDelta)
        else:
            sortedRows = sorted(self.rows, key=lambda row: row[sort_key])

        for row in sortedRows:
            ####### Assign time msg #######
            timeDelta = self.getTimeDelta(row)
            timeMsg = self.convertTimeDeltaToMsg(timeDelta)

            ####### Make a line in list #######
            item = ThreeLineListItem(
                text="Board: " + str(row[4]), # Board Number
                secondary_text="Priority: " + str(row[5]) + " - " + str(row[10]), # Priority
                tertiary_text="Time: " + str(timeMsg), # How long board has been in Kiosk
                on_release=lambda x: self.selectReport(row)
            )
            report_list.add_widget(item)

        print(f"Sorted by: {sort_key}")


#################################################################################
#        - Select report and switch screen
#################################################################################
    def selectReport(self, row):
        GlobalScreenManager.BOARD_CHECKOUT = row
        print("Selected board data:", row)

        MDApp.get_running_app().switchScreen("adminConfirm")