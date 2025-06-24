from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

class GlobalScreenManager(ScreenManager):    
    CURRENT_USER = 0
    CURRENT_MO = ""
    CURRENT_BID = 0
    CURRENT_PRIORITY = 0

    PREVIOUS_SCREEN = ""

    TEMPLATE_REPORTS = [
        {"project": "Project 2", "tech": "Han Solo", "date": "05/04/2025"},
        {"project": "Project 3", "tech": "Chewbaca", "date": "06/02/2024"},
        {"project": "Project 1", "tech": "Luke Skywalker", "date": "12/02/2023"},
    ]

    USERS = [
        "U155759",
        "U312110"
    ]



def GSM():
    return MDApp.get_running_app().root
