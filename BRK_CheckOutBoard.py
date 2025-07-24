from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from BRK_GSM import GlobalScreenManager
import pymssql

class CheckOutBoard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = MDApp.get_running_app().root

    def on_enter(self):
        self.ids.BoardReworkBtn.opacity = 0
        self.ids.BGAReworkBtn.opacity = 0
        self.ids.errorMSG.opacity = 0
        self.ids.AdminCheckoutBtn.opacity = 0
        self.ids.AdminCheckoutBtn.disabled = True
        self.ids.BoardReworkBtn.disabled = True
        self.ids.BGAReworkBtn.disabled = True

#################################################################################
#        - Show checkout options based on permissions
#################################################################################
        if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.REWORK_USERS:
            self.ids.checkOutLabel.opacity = 1
            self.ids.BoardReworkBtn.opacity = 1
            self.ids.BoardReworkBtn.disabled = False
            if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.BGA_USERS:
                self.ids.BGAReworkBtn.opacity = 1
                self.ids.BGAReworkBtn.disabled = False
                if GlobalScreenManager.CURRENT_USER in GlobalScreenManager.ADMIN_USERS:
                    self.ids.AdminCheckoutBtn.opacity = 1
                    self.ids.AdminCheckoutBtn.disabled = False
        else:
            self.ids.errorMSG.text = "You are not registered for Check-Out"
            self.ids.checkOutLabel.opacity = 0
            self.ids.errorMSG.opacity = 1

#################################################################################
#        - Search Kiosk_Table for next Normal board rework if any
#################################################################################
    def findNBRBoard(self):
        try:
            server='USW-SQL30003.rootforest.com'
            user='OvenBakedUsr'
            password='aztmvcjfrizkcpdcehky'
            database='Oven_Bake_Log'
            with pymssql.connect(server, user, password, database) as conn:
                print("Created connection...")
                with conn.cursor() as cursor:
                    print("Successfully connected to SQL database.")

                    cursor.execute("""
                        SELECT TOP 1 * FROM Kiosk_Table
                        WHERE rework_type = 'NBR'
                        ORDER BY priority ASC, time_stamp ASC
                    """)
                    result = cursor.fetchone()
                    print("=================result==============", result)

            # Check that database is not empty
            if result is None:
                raise ValueError("No board found")

            GlobalScreenManager.BOARD_CHECKOUT = result
            GlobalScreenManager.CHECKOUT_USER = GlobalScreenManager.CURRENT_USER
            print("Top Priority task: (CheckOutScreen) ",result)

            MDApp.get_running_app().switchScreen('checkOutConfirm')

        except Exception as e:
            print("No Board in Kiosk")
            print(e)

            self.ids.errorMSG.text = "No NBR Boards in Kiosk"
            self.ids.errorMSG.opacity = 1

            self.ids.checkOutLabel.opacity = 0
            self.ids.BoardReworkBtn.opacity = 0
            self.ids.BGAReworkBtn.opacity = 0
            self.ids.AdminCheckoutBtn.opacity = 0

            self.ids.BoardReworkBtn.disabled = True
            self.ids.BGAReworkBtn.disabled = True
            self.ids.AdminCheckoutBtn.disabled = True

        finally:
            conn.close()


#################################################################################
#        - Search Kiosk_Table for next BGA board rework if any
#################################################################################
    def findBGABoard(self):
        try:
            server='USW-SQL30003.rootforest.com'
            user='OvenBakedUsr'
            password='aztmvcjfrizkcpdcehky'
            database='Oven_Bake_Log'
            with pymssql.connect(server, user, password, database) as conn:
                print("Created connection...")
                with conn.cursor() as cursor:
                    print("Successfully connected to SQL database.")

                    cursor.execute("""
                        SELECT TOP 1 * FROM Kiosk_Table
                        WHERE rework_type = 'BGA'
                        ORDER BY priority ASC, time_stamp ASC
                    """)
                    result = cursor.fetchone()
                    print("=================result==============", result)

            # Check that database is not empty
            if result is None:
                raise ValueError("No board found")

            GlobalScreenManager.BOARD_CHECKOUT = result
            GlobalScreenManager.CHECKOUT_USER = GlobalScreenManager.CURRENT_USER
            print("Top Priority task: (CheckOutScreen) ",result)

            MDApp.get_running_app().switchScreen('checkOutConfirm')

        except Exception as e:
            print("No Board in Kiosk")
            print(e)

            self.ids.errorMSG.text = "No BGA Boards in Kiosk"
            self.ids.errorMSG.opacity = 1

            self.ids.checkOutLabel.opacity = 0
            self.ids.BoardReworkBtn.opacity = 0
            self.ids.BGAReworkBtn.opacity = 0
            self.ids.AdminCheckoutBtn.opacity = 0

            self.ids.BoardReworkBtn.disabled = True
            self.ids.BGAReworkBtn.disabled = True
            self.ids.AdminCheckoutBtn.disabled = True

        finally:
            conn.close()