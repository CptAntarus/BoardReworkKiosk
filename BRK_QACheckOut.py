#################################################################################
#
#       - File: BRK_QACheckOut.py
#       - Author: Dylan Hendrix
#       - Discription: 
#
################################################################################
#
#       - Entry:   
#
#       - Exit:    
#
#################################################################################

import pymssql
import json
import re
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import ThreeLineListItem
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager


class QACheckOut(Screen):
    def on_enter(self):
        print("QACheckOut Screen")
        Clock.schedule_once(self.delayedInit,0.1)

    def delayedInit(self,dt):
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
                    cursor.execute("""
                        SELECT * FROM Kiosk_Table
                        WHERE rework_status = %s
                        ORDER BY priority DESC
                        """, ("WQA",)) 
                    self.rows = cursor.fetchall()

                    # Check if kiosk is empty
                    if not self.rows:
                        print("Database is empty")
                        GlobalScreenManager.noBoardsFlag = "NONE"
                        MDApp.get_running_app().switchScreen("noBoardScreen")

                except Exception as e:
                    print("Error sorting reports:", e)

                finally:
                    self.makeList(GlobalScreenManager.CURRENT_USER)


    def getTimeDelta(self, row):
        nowMonth = int(datetime.now().strftime("%m"))
        nowDay = int(datetime.now().strftime("%d"))

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
    def makeList(self, user):
        report_list = self.ids.inProgressReportList
        report_list.clear_widgets()

        sortedRows = sorted(self.rows, key=self.getTimeDelta)

        for row in sortedRows:
            ####### Assign time msg #######
            timeDelta = self.getTimeDelta(row)
            timeMsg = self.convertTimeDeltaToMsg(timeDelta)

            ####### Make a line in list #######
            item = ThreeLineListItem(
                text="Board: " + str(row[4]), # Board Number
                secondary_text="Priority: " + str(row[5]) + " - " + str(row[10]), # Priority & RW Type
                tertiary_text="Time: " + str(timeMsg), # How long board has been in Kiosk
                on_release= lambda x: self.selectReport(row)
            )
            report_list.add_widget(item)

    def selectReport(self, row):
        GlobalScreenManager.CHECKOUT_USER = GlobalScreenManager.CURRENT_USER
        GlobalScreenManager.BOARD_CHECKOUT = row
        print("Selected board data:", row) 

        MDApp.get_running_app().switchScreen("checkOutConfirm")