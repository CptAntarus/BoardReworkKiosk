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
