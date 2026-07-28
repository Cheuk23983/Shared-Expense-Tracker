# Purpose: This program is to create a window for user to create a tirp JSON file to add expenses.
# Author: Hubert Kwan
# Date: 27/07/2026
# Version: 1.0


# import libraries and modules
import os
import json
import customtkinter as ctk
from tkinter import messagebox

# create class for trip creation
class TripCreationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Trip Creation Window")
        self.root.geometry("450x650")
        
        self.folder_path = "trips"
        self.added_members = []
        self.memeber_list_widgets = []
        
        # configure layout grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        
        #Build the GUI layout
        self.create_widgets()
        
        
        def create_widgets(self):
            '''Build the form layout and input for creaeting a trip'''
            # title label
            self.lbl_title = ctk.CTkLabel(self.root, text="Create a Trip", font=ctk.CTkFont(siz=20, weight="bold"))
            self.lbl_title.grid(ro=0, column=0, columnspan=2, pady=(20,10))
            
            # trip name label and entry box
            self.lbl_trip_name = ctk.CTkLabel(self.root, text="Trip Name:")
            self.lbl_trip_name.grid(row=1, column=0, padx=15, pady=8, sticky="e")
            self.entry_trip_name = ctk.CTkEntry(self.root, placeholder_text="e.g. Queenstown trip", justify="center")
            self.entry_trip_name.grid(eow=1, column=1, padx=15, pady=8, sticky="ew")
