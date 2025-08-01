#################################################################################
#
#       - File: BRK_InOutScreen.py
#       - Author: Dylan Hendrix
#       - Discription: This is the screen that sends the user either to the
#                       input or output functionalities
#
################################################################################
#
#       - Entry:   BRK_CloseDoor.py
#
#       - Exit:    BRK_InOutScreen.py
#
#################################################################################

import pymssql
import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

from BRK_GSM import GlobalScreenManager


class InOutScreen(Screen):
    def on_enter(self):
        with open("BRK_Creds.json") as f:
            config = json.load(f)

        with pymssql.connect(
            server=config["SERVER"],
            user=config["USER"],
            password=config["PASSWORD"], 
            database=config["DATABASE"]
        ) as conn:

            with conn.cursor() as cursor:
                print("Successfully connected to SQL database.")

                try:
                    cursor.execute("""
                        SELECT * FROM Kiosk_Table
                        WHERE rework_status = %s
                        """, ("Passed QA",))
                    self.rows = cursor.fetchall()

                    # Check for any completed boards
                    if not self.rows:
                        self.ids.CompletedBtn.opacity = 0
                        self.ids.CompletedBtn.disabled = True
                    else:
                        self.ids.CompletedBtn.opacity = 1
                        self.ids.CompletedBtn.disabled = False

                except Exception as e:
                    print("Error sorting reports:", e)
