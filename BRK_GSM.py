from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

class GlobalScreenManager(ScreenManager):    
    CURRENT_USER = 0
    CURRENT_MO = 0
    CURRENT_BID = 0
    CURRENT_PRIORITY = 0
    CURRENT_RW_TYPE = 0
    HASH_KEY = 0
    BOARD_CHECKOUT = 0

    SCREEN_HIST = []

    # 3 rows, 4 cols, 5 slots/box
    # KIOSK_BOXES = [[[None for _ in range(3)] for _ in range(4)] for _ in range(5)]
    KIOSK_BOXES = [[None for _ in range(20)] for _ in range(3)]
    # KIOSK_BOXES = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]

    USERS = []
    REWORK_USERS = []
    BGA_USERS = []
    ADMIN_USERS = []



def GSM():
    return MDApp.get_running_app().root
