# Purpose: This program is to create a window for user to create a trip JSON file to add expenses.
# Author: Hubert Kwan
# Date: 27/07/2026
# Version: 1.1

# import libraries and modules
import os
import json
import customtkinter as ctk
from datetime import datetime
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
        self.root.grid_columnconfigure(1, weight=2)
        
        # Build the GUI layout
        self.create_widgets()
        
        
    def create_widgets(self):
        '''Build the form layout and input for creating a trip'''
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
        
        self.btn_add_member = ctk.CTkButton(self.member_input_frame, text="Add", width=60, command=self.add_member)
        self.btn_add_member.pack(side="right")
        
        # scrollable frame to list all added members
        self.lbl_added_members = ctk.CTkLabel(self.root, text="Added Member:")
        self.lbl_added_members.grid(row=6, column=0, padx=15, pady=8, sticky="ne")
        
        self.scrollable_member_frame = ctk.CTkScrollableFrame(self.root, height=110, label_text="Group Members")
        self.scrollable_member_frame.grid(row=6, column=1, padx=15, pady=8, sticky="nsew")
        
        # actions buttons "back" & "create"
        self.action_btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.action_btn_frame.grid(row=8, column=0, columnspan=2, pady=(10, 20))
        
        self.btn_back = ctk.CTkButton(self.action_btn_frame, text="Back", fg_color="grey", hover_color="#555555", width=100, command=self.back_btn_on_click)
        self.btn_back.pack(side="left", padx=10)
        
        self.btn_create = ctk.CTkButton(self.action_btn_frame, text="Create", fg_color="#0080FF", width=100, command=self.create_btn_on_click)
        self.btn_create.pack(side="right", padx=10)
        
        
    def show_error(self, message):
        '''Display error message when invalid input'''
        messagebox.showerror("Error", message)
    
            
    def add_member(self):
        '''Add a new member to the list'''
        input_name = self.entry_member_name.get().strip()

        if input_name == "":
            self.show_error("Member name cannot be blank!")
            return
            
        existing_lower = [m.lower() for m in self.added_members]
        if input_name.lower() in existing_lower:
            self.show_error("Member is already added!")
            return
        
        self.added_members.append(input_name)
        self.entry_member_name.delete(0, "end")
        self.update_member_list()
        
        
    def update_member_list(self):
        '''Update member list when a new member name is added.'''
        for widget in self.memeber_list_widgets:
            widget.destroy()
        self.memeber_list_widgets = []
        
        for name in self.added_members:
            member_list = ctk.CTkFrame(self.scrollable_member_frame, fg_color="transparent")
            member_list.pack(fill="x", pady=2)
            
            lbl_name = ctk.CTkLabel(member_list, text=f"{name}", font=ctk.CTkFont(size=13))
            lbl_name.pack(side="left", padx=5)
            

    def validate_input(self):
        '''validating input fields before create a trip.'''
        name = self.entry_trip_name.get().strip()
        start_date_str = self.entry_start_date.get().strip()
        end_date_str = self.entry_end_date.get().strip()
        
        if name == "":
            self.show_error("Trip name cannot be blank!")
            return False
            
        if start_date_str == "" or end_date_str == "":
            self.show_error("Start date and End date cannot be blank!")
            return False
            
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

            if end_date < start_date:
                self.show_error("End date cannot be before start date!")
                return False
        except ValueError:
            self.show_error("Dates must be in dd/mm/yyyy format!")
            return False
        
        if len(self.added_members) == 0:
            self.show_error("You must add at least 1 member to the trip!")
            return False
        
        return True

        
    def create_btn_on_click(self):
        '''save the trip data into a json file'''
        if not self.validate_input():
            return
        
        trip_name = self.entry_trip_name.get().strip()
        
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        
        clean_file_name = trip_name.lower().replace(" ", "_") + ".json"
        file_path = os.path.join(self.folder_path, clean_file_name)
        
        if os.path.exists(file_path):
            confirm = messagebox.askyesno(
                "Overwrite Warning", 
                f"A trip named '{trip_name}' already exists!\nDo you want to overwrite it?"
            )
            if not confirm:
                return
        
        trip_data = {
            "name": trip_name,
            "base_currency": self.option_currency.get(),
            "start_date": self.entry_start_date.get().strip(),
            "end_date": self.entry_end_date.get().strip(),
            "members": self.added_members,
            "expenses": []
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(trip_data, f, indent=4)
            messagebox.showinfo("Success", f"Trip '{trip_name}', successfully created")
        except Exception as e:
            self.show_error(f"Could not save trip file:{e}")
            
    
    def back_btn_on_click(self):
        '''Return to the launcher window'''
        # currently its a palceholder that will printed a message in terminal 
        print("Back to main menu")
        
        
root = ctk.CTk()
app = TripCreationWindow(root)
root.mainloop()
