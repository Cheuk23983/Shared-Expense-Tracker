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
        
    def create_widgets(self):
        '''Create all widgets need for the window.'''
        # Title of the window
        self.title_label = ctk.CTkLabel(self, text="Group Expense Tracker", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        # Frame for top buttons
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=0, column=0, padx=20, pady=5, sticky="ew")
        # select button
        self.select_mode_btn - ctk.CTkButton(self.action_frame, text="Select", width=80)
        self.select__mode_btn.pack(side="left")
        # add trip button
        self.new_trip_btn = ctk.CTkButton(self.action_frame, text="+ New Trip", command=self.create_trip)
        self.new_trip_btn.pack(side="right")
        
        
        
        
        