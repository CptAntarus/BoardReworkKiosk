from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager


class AdminEnterUser(Screen):
    def on_enter(self):
        print("Admin Enter User")

    def editText(self, character):
        inputField = self.ids.newUser

        if character == "Space":
            inputField.text += " "
        elif character == "Backspace":
            inputField.text = inputField.text[:-1]
        else:
            inputField.text += character

    def confirmNewUser(self):
        uNum = self.ids.newUser.text
        if uNum in GlobalScreenManager.USERS:
            print(f"Valid user: {uNum}")
            GlobalScreenManager.CHECKOUT_USER = self.ids.newUser.text.strip()
            print(f"uNum: {uNum}")
            MDApp.get_running_app().switchScreen('checkOutConfirm')
            
        else:
            print("Invalid User")
            self.ids.newUser.text=""
            Clock.schedule_once(self.clearInput,0.1)

    def clearInput(self, dt):
        self.ids.newUser.text=""
        self.ids.newUser.focus=True
