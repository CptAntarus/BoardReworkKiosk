from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

class GlobalScreenManager(ScreenManager):    
    CURRENT_USER = 0
    CURRENT_MO = 0
    CURRENT_BID = 0
    CURRENT_PRIORITY = 0
    HASH_KEY = 0

    PREVIOUS_SCREEN = ""

    # 3 rows, 4 cols, 5 slots/box
    KIOSK_BOXES = [[[None for _ in range(3)] for _ in range(4)] for _ in range(5)]
    #KIOSK_BOXES = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]

    USERS = [
        "U155759",
        "U312110",
        "U313773"
    ]



def GSM():
    return MDApp.get_running_app().root
