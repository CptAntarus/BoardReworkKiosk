#################################################################################
#
#       - File: BRK_SelectCheckout.py
#       - Author: Dylan Hendrix
#       - Discription: This is the screen that sends the user either to the
#                       new checkout or checkout a board they've worked on before
#
################################################################################
#
#       - Entry:   
#
#       - Exit:    
#
#################################################################################

from kivy.uix.screenmanager import Screen

from BRK_GSM import GlobalScreenManager


class SelectCheckout(Screen):
    def on_enter(self):    
        # Disable all buttons before permissions validation
        self.ids.NewReworkBtn.opacity = 0
        self.ids.InProgressBtn.opacity = 0
        self.ids.AdminCheckoutBtn.opacity = 0
        self.ids.QACheckoutBtn.opacity = 0
        self.ids.errorMSG.opacity = 0

        self.ids.NewReworkBtn.disabled = True
        self.ids.InProgressBtn.disabled = True
        self.ids.AdminCheckoutBtn.disabled = True
        self.ids.QACheckoutBtn.disabled = True

#################################################################################
#        - Show checkout options based on permissions
#################################################################################
        if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.REWORK_USERS:
            self.ids.SelectCheckOutLabel.opacity = 1
            self.ids.NewReworkBtn.opacity = 1
            self.ids.NewReworkBtn.disabled = False
            self.ids.InProgressBtn.opacity = 1
            self.ids.InProgressBtn.disabled = False
        else:
            self.ids.errorMSG.text = "You are not registered for Check-Out"
            self.ids.SelectCheckOutLabel.opacity = 0
            self.ids.errorMSG.opacity = 1

        if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.ADMIN_USERS:
            self.ids.AdminCheckoutBtn.opacity = 1
            self.ids.AdminCheckoutBtn.disabled = False
        if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.QA_USERS:
            self.ids.QACheckoutBtn.opacity = 1
            self.ids.QACheckoutBtn.disabled = False
