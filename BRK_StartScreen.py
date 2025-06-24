from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from BRK_GSM import GlobalScreenManager, GSM
from kivy.clock import Clock


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = GSM()

    def on_enter(self):
        Clock.schedule_once(self.set_focus, 0.1)

    def set_focus(self, dt):
        self.ids.EmpID.focus = True

    def validateUsr(self, uNum):
        if uNum in GlobalScreenManager.USERS:
            print(f"Valid user: {uNum}")
            self.sm = MDApp.get_running_app().root
            self.sm.PREVIOUS_SCREEN = 'startScreen'
            GlobalScreenManager.CURRENT_USER = uNum
            print(f"uNum: {uNum}")
            self.sm.current = 'inOutScreen'
        else:
            print("Invalid User")
            self.ids.EmpID.text=""
            Clock.schedule_once(self.clearInput,0.1)

    def clearInput(self, dt):
        self.ids.EmpID.text=""
        self.ids.EmpID.focus=True