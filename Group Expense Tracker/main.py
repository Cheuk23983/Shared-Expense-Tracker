# Purpose: A controller to connect different components.
# Author: Hubert Kwan
# Date: 12/08/2026
# Version: 1.0


import os
import importlib
import customtkinter as ctk

# Import component classes from filenames
MainMenuFrame = importlib.import_module("component_1_main_Menu(launcher)").MainMenuFrame
TripCreationWindow = importlib.import_module("component_2_trip_creation_window").TripCreationWindow
TripDashboard = importlib.import_module("component_3_trip_dashboard").TripDashboard
ExpenseFormWindow = importlib.import_module("component_4_expense_window").ExpenseFormWindow


class TrackerController:
    '''Controller to manage windows pop=up and trip path'''
    def __init__(self):
        self.root = self.root
        self.active_trip_file = None
        self.show_launcher_view()
        
    
    def clean_window(self):
        for widget in self.root.winfo_chiilren():
            widget.destroy()
