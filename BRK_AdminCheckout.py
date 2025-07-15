from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineListItem
import sqlite3
import re

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

        conn = sqlite3.connect('KioskDB.db')
        cursor = conn.cursor()

        # Refresh the list
        report_list = self.ids.reportList
        report_list.clear_widgets()

        try:
            cursor.execute(f"""
                SELECT * FROM checkins
                ORDER BY {sort_key} ASC
            """)

            rows = cursor.fetchall()

            # Check if kiosk is empty
            if not rows:
                print("Database is empty")
                report_list.add_widget(
                    ThreeLineListItem(
                        text="No Boards In Kiosk",
                        secondary_text="Check back later",
                        tertiary_text="",
                        on_release=lambda *args: None
                    )
                )
                return


            for row in rows:
                item = ThreeLineListItem(
                    text="Board: " + str(row[4]) + " " + str(row[10]), # Board Number
                    secondary_text="Priority: " + str(row[5]), # Priority
                    tertiary_text="Time: " + str(row[6]), # Entry Time
                    on_release=self.make_select_handler(row)
                )
                report_list.add_widget(item)

            print(f"Sorted by: {sort_key}")

        except Exception as e:
            print("Error sorting reports:", e)

        finally:
            conn.close()

    def make_select_handler(self, row_data):
        return lambda *args: self.selectReport(row_data)

    def selectReport(self, row):
        GlobalScreenManager.BOARD_CHECKOUT = row
        print("Selected board data:", row)

        MDApp.get_running_app().switchScreen("checkOutConfirm")