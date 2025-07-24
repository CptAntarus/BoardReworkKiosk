from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
from BRK_GSM import GlobalScreenManager
import pymssql


class CheckOutConfirm(Screen):
    def on_enter(self):
        print("==========================================")
        # print("Top Priority task: (CheckOutConfirm) ",GlobalScreenManager.BOARD_CHECKOUT)

        Clock.schedule_once(self.delayedInit,0.1)

    def delayedInit(self, dt):
        data = GlobalScreenManager.BOARD_CHECKOUT

        print("SELECTED BOARD:", data)

        self.ids.checkOutConfirmUNum.text = str(GlobalScreenManager.CHECKOUT_USER)
        self.ids.checkOutConfirmMONum.text = str(data[3])       # MO
        self.ids.checkOutConfirmBoardID.text = str(data[4])     # Board Number
        self.ids.checkOutConfirmPriority.text = str(data[5])    # Priority
        self.ids.checkOutConfirmRWType.text = str(data[10])     # Rework Type

        self.hashKey = str(data[1])

    def confirmCheckOut(self):
        now = datetime.now()
        data = GlobalScreenManager.BOARD_CHECKOUT

#################################################################################
#        - Copy over to Rework_Table
#################################################################################
        server='USW-SQL30003.rootforest.com'
        user='OvenBakedUsr'
        password='aztmvcjfrizkcpdcehky'
        database='Oven_Bake_Log'
        with pymssql.connect(server, user, password, database) as conn:
            print("Created connection...")
            with conn.cursor() as cursor:
                print("Successfully connected to SQL database.")
                cursor.execute('''
                    INSERT INTO Rework_Table (hash_key, [u-num], mo, board_id, priority, time_stamp, in_out_status, rework_type, rework_status)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',
                    (   
                        data[1], # hash_key
                        GlobalScreenManager.CHECKOUT_USER, # U-Number
                        data[3], # MO Number
                        data[4], # Board ID
                        data[5], # Priority
                        now.strftime("%m-%d-%Y %H:%M:%S"),
                        "OUT",
                        data[10], # rework_type
                        data[11]  # rework_status
                    )
                )
                conn.commit()

            # Print Database
                print("Rework_Table =====================================")
                cursor.execute('SELECT * FROM Rework_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

#################################################################################
#        - Delete from Kiosk_Table
#################################################################################
                cursor.execute("DELETE FROM Kiosk_Table WHERE hash_key = %s", (data[1],))
                conn.commit()

         # Print Database
                print("Kiosk_Table =====================================")
                cursor.execute('SELECT * FROM Kiosk_Table')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

#################################################################################
#       - Remove from KIOSK_BOXES
#################################################################################
        try:
            numRows = len(GlobalScreenManager.KIOSK_BOXES)
            numCols = len(GlobalScreenManager.KIOSK_BOXES[0]) if numRows > 0 else 0
            removed = False

            for i in range(numRows):
                for j in range(numCols):
                    if GlobalScreenManager.KIOSK_BOXES[i][j] == data[1]:
                        GlobalScreenManager.KIOSK_BOXES[i][j] = None
                        removed = True
                        break
                if removed:
                    break

        except Exception as e:
            print("Error repopulating kiosk boxes:",e)

        finally:
            print("KIOSK_BOXES =======================================")
            print(GlobalScreenManager.KIOSK_BOXES)

#################################################################################
#       - Go to board out screen
#################################################################################
        MDApp.get_running_app().switchScreen('closeDoor')
