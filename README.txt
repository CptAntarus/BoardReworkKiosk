######################################################################
#                     Board Rework Kiosk README                      #
######################################################################

[File Organization]
 - BoardReworkKiosk -----------	(Top Level Directory)
 	- BRK_main.py ---------	(Contains the main MDApp class)
	- BRK_GSM.py ---------- (Contains a class for storing global variables)
 	- BRK_Format.kv -------	(Controls the format of each screen)
	- BRK_*.py ------------	(Files controling different screens)

 - Note: Headers contian notes about 'Entry' and 'Exit' files. Entry lists files that can send the user to the current file. Exit lists files the user can be sent to from the current file. The back button takes the user back one screen.


[Imports]
 - Native to Pyton:
	- re ------------------- (Regex, used to validate inputs)
	- datetime ------------- (Used for recording date and time in SQL)

 - Need to be installed:
 	- Kivy ----------------- (GUI package)
	- KivyMD --------------- (GUI package)
	- pymssql -------------- (For accessing databases)
	- Builder -------------- (Kivy package used to load .kv files)

 - Custom:
	- GlobalScreenManager -- (Imported at the top of each file to give access to global variables)


[Running the App]
 - Activate the environment: (From BoardReworkKiosk)
	- Windows:	".\BRK_Env\Scripts\activate"
	- Raspberry Pi: "source BRK/bin/activate"

 - Run main file:
	- "python BRK_main.py"


[Data Bases]
 - There are 3 datatables all within the "Oven_Bake_Log" database: "User_Table", "HISTORY", and "KIOSK". The history table stores a log of every transaction with the kiosk whether a board is put in, or taken out. While the kiosk table serves as a backup to the kiosk if it were reboot after a power loss or a crash. The kiosk table also stores the indicies where each board is located so that the boards are not misplaced after a reboot. The User_Table stores a list of all the valid users and their assosiated permissions.

- See Benjamin Barger for further details


[Screen Navigation]
 - In order to simplify screen navigation I have two functions within BRK_main.py: "switchScreen", and "backButton". 'switchscreen' takes 1 argument, the new screen, saves the current screen to a history variable, and then switches to the new screen. 'backbutton' does not need any arguements passed to it because it pops the to item off of the history variable to and uses that to set the new screen.


[Credentials]
 - Credentials for the database are stored in a seperate file. See Benjamin Barger for further detials.
