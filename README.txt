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
 - There are 4 datatables all within the "Oven_Bake_Log" database: "User_Table", "History_Table", "Rework_Table", and "Kiosk_Table". 
	-> User_Table:    stores a list of all the valid users and their assosiated permissions.
	-> History_Table: stores all the logs after a board is completed and checked out.
	-> Rework_Table:  stores a log of every transaction with the drybox whether a board is put in, or taken out, as well as the status. Once the baord is completed and checked out all logs for that board will then be moved to History_Table.
	-> Kiosk_Table:   serves as a backup for the kiosk if the system reboots after a power loss or a crash. It also stores the indicies where each board is located so that the boards are not misplaced after a reboot.

- See Benjamin Barger for further details


[Screen Navigation]
 - In order to simplify screen navigation I have two functions within BRK_main.py: "switchScreen", and "backButton". 
 	-> switchscreen: takes 1 argument, the new screen. It saves the current screen to "SCREEN_HIST", and then switches to the new screen. 
	-> backbutton:   pops the top item from the "SCREEN_HIST" and sets the new screen with the 'popped' value.


[Credentials]
 - Credentials for the database are stored seperate file from the app. See Benjamin Barger for further detials.


[Launching GUI]
 - The Pi is set up with a script that runs on startup. This located in the local crontab. This can be accessed with:
	-> "crontab -e"
	-> Look for @reboot /home/washer/Rework_GUI/BoardReworkKiosk/runGUI.sh
	
 - This script assumes the directory names. (Adjust accordingly):

Script:
"""
#!/bin/bash

# This is the script to run the GUI

sleep  7

export Display=:0
export XAUTHORITY=/home/washer/.Xauthority

echo "Activating Env..."
source ~/Rework_GUI/BoardReworkKiosk/ENV_BRK/bin/activate

echo "Starting GUI..."
python ~/Rework_GUI/BoardReworkKiosk/BRK_main.py
"""