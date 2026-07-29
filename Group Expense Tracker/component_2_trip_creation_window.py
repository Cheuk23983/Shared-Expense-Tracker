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
        self.lbl_title = ctk.CTkLabel(self.root, text="Create a Trip", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.grid(row=0, column=0, columnspan=2, pady=(20,10))
        
        # trip name label and entry box
        self.lbl_trip_name = ctk.CTkLabel(self.root, text="Trip Name:")
        self.lbl_trip_name.grid(row=1, column=0, padx=15, pady=8, sticky="e")
        self.entry_trip_name = ctk.CTkEntry(self.root, placeholder_text="e.g. Queenstown trip", justify="center")
        self.entry_trip_name.grid(row=1, column=1, padx=15, pady=8, sticky="ew")
        
        # base currency option menu
        self.lbl_currency = ctk.CTkLabel(self.root, text="Base Currency:")
        self.lbl_currency.grid(row=2, column=0, padx=15, pady=8, sticky="e")
        self.option_currency = ctk.CTkOptionMenu(self.root, values=["NZD", "AUD", "USD", "EUR", "GBP", "JPY"])
        self.option_currency.grid(row=2, column=1, padx=15, pady=8, sticky="w")
        
        # start date label and entry box
        self.lbl_start_date = ctk.CTkLabel(self.root, text="Start Date:")
        self.lbl_start_date.grid(row=3, column=0, padx=15, pady=8, sticky="e")
        self.entry_start_date = ctk.CTkEntry(self.root, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_start_date.grid(row=3, column=1, padx=15, pady=8, sticky="ew")
        
        # end date label and entry box
        self.lbl_end_date = ctk.CTkLabel(self.root, text="End Date:")
        self.lbl_end_date.grid(row=4, column=0, padx=15, pady=8, sticky="e")
        self.entry_end_date = ctk.CTkEntry(self.root, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_end_date.grid(row=4, column=1, padx=15, pady=8, sticky="ew")
        
        # member entry box and "add" button
        self.lbl_member = ctk.CTkLabel(self.root, text="Member Name:")
        self.lbl_member.grid(row=5, column=0, padx=15, pady=8, sticky="e")
        
        self.member_input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.member_input_frame.grid(row=5, column=1, padx=15, pady=8, sticky="ew")
        
        self.entry_member_name = ctk.CTkEntry(self.member_input_frame, placeholder_text="Enter name", justify="center")
        self.entry_member_name.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_add_member = ctk.CTkButton(self.member_input_frame, text="Add", width=60)
        self.btn_add_member.pack(side="right")
        
        # scrollable frame to list all added members
        self.lbl_added_members = ctk.CTkLabel(self.root, text="Added Member:")
        self.lbl_added_members.grid(row=6, column=0, padx=15, pady=8, sticky="ne")
        
        self.scrollable_member_frame = ctk.CTkScrollableFrame(self.root, height=110, label_text="Group Members")
        self.scrollable_member_frame.grid(row=6, column=1, padx=15, pady=8, sticky="nsew")
        
        # actions buttons "back" & "create"
        self.action_btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.action_btn_frame.grid(row=8, column=0, columnspan=2, pady=(10, 20))
        
        self.btn_back = ctk.CTkButton(self.action_btn_frame, text="Back", fg_color="grey", hover_color="#555555", width=100)
        self.btn_back.pack(side="left", padx=10)
        
        self.btn_create = ctk.CTkButton(self.action_btn_frame, text="Create", fg_color="#0080FF", width=100)
        self.btn_create.pack(side="right", padx=10)
            
root =ctk.CTk()
app = TripCreationWindow(root)
root.mainloop()
