#################################################################################
#
#       - File: BRK_AdminConfirm.py
#       - Author: Dylan Hendrix
#       - Discription: This screen controls the logic when an admin checks out
#                       a board
#
################################################################################
#
#       - Comes From:   BRK_AdminCheckout.py
#
#       - Goes To:      BRK_CheckOutConfirm.py,
#                       BRK_AdminEnterUser.py
#
#################################################################################

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

from BRK_GSM import GlobalScreenManager


class AdminConfirm(Screen):
    def on_enter(self):
        print("Admin Confirm")


    def CheckoutForSelf(self):
        MDApp.get_running_app().switchScreen("checkOutConfirm")
        GlobalScreenManager.CHECKOUT_USER = GlobalScreenManager.CURRENT_USER
    

    def CheckoutForOther(self):
        MDApp.get_running_app().switchScreen("adminEnterUser")
