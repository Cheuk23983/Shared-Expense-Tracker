
# Purpose: This window allow users to enter expense details (title, amount, date, payer, description, and member spliting boxes ) to a trip json file.
# Author: Hubert Kwan
# Date: 10/08/2026
# Version: 1.0


# import libraries and modules
import os 
import json
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

# Set up app appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ExpenseFormWindow:
    def __init__(self, root, file_path="trip/japan.json"):
        '''initialse the form window, with loading trip data and the UI'''
        self.root = root
        self.root.title("Expense Management Window")
        self.root.geometry("400x650")
        # self.top.lift()
        
        self.file_path = file_path
        self.trip_info_dict = {}
        self.members_list = []
        # dictory to store expense split variables
        self.checkbox_widget = {}
        
        if os.path.exists(self.file_path):
            self.load_trip_file()
        else:
            self.members_list = ["Alice", "Bob", "Charlie"]

        # Configure pop-up window grid columns
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Build all form input fields
        self.create_widgets()
        
    
    def load_trip_file(self):
        '''Loads member list safely from json file'''
        try:
            with open(self.file_path, "r", encoding="utf-8") as file_data:
                self.trip_info_dict = json.load(file_data)
        except FileNotFoundError:
            self.show_error("Could not find the trip file to load members")
            
    
    def create_widgets(self):
        '''Create all input fields, labels, option menus, and buttons '''
        # Heading label
        self.lbl_window_title = ctk.CTkLabel(self.root, text="Add/Edit Expense", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_window_title.grid(row=0, column=0, columnspan=2, pady=(15, 10))
        # Expense title label
        self.lbl_expense_title = ctk.CTkLabel(self.root, text="Title", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_expense_title.grid(row=1, column=0, columnspan=2, padx=20, pady=(5, 2), stick="w")
        # Expense title entry box
        self.entry_expense_title = ctk.CTkEntry(self.root, placeholder_text="e.g. Dinner in Sushiro", justify="center")
        self.entry_expense_title.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="ew")
        # Amount label
        self.lbl_amount = ctk.CTkLabel(self.root, text="Title", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_amount.grid(row=1, column=0, columnspan=2, padx=20, pady=(5, 2), stick="w")
        # Amount entry box
        self.entry_amount = ctk.CTkEntry(self.root, placeholder_text="e.g. Dinner in Sushiro", justify="center")
        self.entry_amount.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="ew")


root = ctk.CTk()
app = ExpenseFormWindow(root)
root.mainloop()
