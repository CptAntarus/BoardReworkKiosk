#################################################################################
#
#       - File: BRK_QACheckOut.py
#       - Author: Dylan Hendrix
#       - Discription: 
#
################################################################################
#
#       - Entry:   
#
#       - Exit:    
#
#################################################################################

import pymssql
import json
import re
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import ThreeLineListItem

from BRK_GSM import GlobalScreenManager


class QACheckOut(Screen):
    def on_enter(self):
        print("QACheckOut Screen")