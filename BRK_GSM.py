#################################################################################
#
#       - File: BRK_GSM.py
#       - Author: Dylan Hendrix
#       - Discription: Class used to store and reference global variables
#
#################################################################################

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager


class GlobalScreenManager(ScreenManager):
    # Global Variables
    CURRENT_USER = 0
    CURRENT_MO = 0
    CURRENT_BID = 0
    CURRENT_PRIORITY = 0
    CURRENT_RW_TYPE = 0
    HASH_KEY = 0
    BOARD_CHECKOUT = 0
    CURRENT_POS_X = 0
    CURRENT_POS_Y = 0
    CHECKOUT_USER = 0
    CURRENT_RW_STATUS = 0
    noBoardsFlag = ""
    CHECKOUT_FLAG = ""

    # List used for screen navigation
    SCREEN_HIST = []

    # Array to store the rows and cols of the dry box
    KIOSK_BOXES = [[None for _ in range(20)] for _ in range(3)]

    # Stores the different lists of users by access level
    USER_NAMES = {}
    USERS = []
    REWORK_USERS = []
    BGA_USERS = []
    QA_USERS = []
    ADMIN_USERS = []


def GSM():
    return MDApp.get_running_app().root
