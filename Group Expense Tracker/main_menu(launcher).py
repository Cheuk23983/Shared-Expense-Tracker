# Purpose: This program is the first component of the tracker project. The Component included function to manage trips. 
# Author: Hubert Kwan
# Date: 21/07/2026
# Version: 1.0

# import customtkinter module
import customtkinter as ctk

# Set global default appearance mode and efault color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# launcher class
class MainMenuFrame:
    '''Launcher window for the tracker'''
    def __init__(self, root, select_trip, create_trip):
        self.root = root
        self.root.title("Group Expense Tracker")
        self.root.resizeable(False,False)
        self.select_trip = select_trip
        self.create_trip = create_trip
        
        # config frame grid layout
        self.root.grid_columnconfig(0,weight=1)
        self.root.grid_rowconfig(2, weight=1)
        
        # make the GUI widgets
        self.create_widgets()
        


        
        
        
        
        