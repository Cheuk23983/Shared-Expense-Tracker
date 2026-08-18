# Purpose: This program is to create a window for user to create a trip JSON file to add expenses.
# Author: Hubert Kwan
# Date: 19/08/2026
# Version: 2.0

# 

# import libraries and modules
import os
import json
import re
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

# Optional import for DatePicker extension
try:
    from tkcalendar import DateEntry
    HAS_TKCALENDAR = True
except ImportError:
    HAS_TKCALENDAR = False
    
# Set up app appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# create class for trip creation
class TripCreationWindow:
    def __init__(self, root, mode="create_trip", file_path=None):
        self.root = root
        self.mode = mode
        self.file_path = file_path
        
        # added a mode condition for edit trip details
        if self.mode == "manage_members":
            self.root.title("Manage Trip Members")
        elif self.mode == "edit_trip_details":
            self.root.title("Edit Trip Details")
        else:
            self.root.title("Trip Creation Window")
            
        self.root.geometry("480x700")
        
        self.folder_path = "trips"
        self.added_members = []
        self.memeber_list_widgets = []
        self.trip_info_dict = {}
        
        # callback function assigned from main program
        self.on_back_callback = None
        self.on_trip_created_callback = None
        
        # configure layout grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        
        # Pre-load data if running in manage_members or edit_trip_details mode
        if (self.mode == "manage_members" or self.mode == "edit_trip_details") and self.file_path != None and os.path.exists(self.file_path) == True:
            self.load_existing_trip_data()

        # Build the GUI layout
        self.create_widgets()

    def load_existing_trip_data(self):
        '''Loads existing trip details'''
        if self.file_path == None:
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.trip_info_dict = json.load(f)
                self.added_members = list(self.trip_info_dict.get("members", []))
        except FileNotFoundError:
            self.show_error(f"Could not find file: {self.file_path}")

    def create_widgets(self):
        '''Build the form layout and input for creating or editing a trip'''
        if self.mode == "manage_members":
            heading_text = "Manage Trip Members"
        elif self.mode == "edit_trip_details":
            heading_text = "Edit Trip Details"
        else:
            heading_text = "Create a Trip"
            
        self.lbl_title = ctk.CTkLabel(self.root, text=heading_text, font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.grid(row=0, column=0, columnspan=2, pady=(15, 10))
        
        # trip name label and entry box
        self.lbl_trip_name = ctk.CTkLabel(self.root, text="Trip Name:")
        self.lbl_trip_name.grid(row=1, column=0, padx=15, pady=6, sticky="e")
        self.entry_trip_name = ctk.CTkEntry(self.root, placeholder_text="e.g. Queenstown trip", justify="center")
        self.entry_trip_name.grid(row=1, column=1, padx=15, pady=6, sticky="ew")
        
        self.lbl_currency = ctk.CTkLabel(self.root, text="Base Currency:")
        self.lbl_currency.grid(row=2, column=0, padx=15, pady=6, sticky="e")
        # Included more currency options
        world_currencies = [
            "NZD", "AUD", "USD", "EUR", "GBP", "JPY", "CAD", "CHF", "CNY", "HKD", 
            "SGD", "SEK", "KRW", "NOK", "MXN", "INR", "BRL", "ZAR", "RUB", "THB"
        ]
        self.option_currency = ctk.CTkOptionMenu(self.root, values=world_currencies)
        self.option_currency.grid(row=2, column=1, padx=15, pady=6, sticky="w")
        
        self.lbl_start_date = ctk.CTkLabel(self.root, text="Start Date:")
        self.lbl_start_date.grid(row=3, column=0, padx=15, pady=6, sticky="e")
        
        self.start_date_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.start_date_frame.grid(row=3, column=1, padx=15, pady=6, sticky="ew")
        
        self.entry_start_date = ctk.CTkEntry(self.start_date_frame, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_start_date.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # added a button to open date picker for start date
        self.btn_pick_start = ctk.CTkButton(self.start_date_frame, text="📅", width=35, command=lambda: self.open_date_picker(self.entry_start_date))
        self.btn_pick_start.pack(side="right")
        
        self.lbl_end_date = ctk.CTkLabel(self.root, text="End Date:")
        self.lbl_end_date.grid(row=4, column=0, padx=15, pady=6, sticky="e")
        
        self.end_date_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.end_date_frame.grid(row=4, column=1, padx=15, pady=6, sticky="ew")
        
        self.entry_end_date = ctk.CTkEntry(self.end_date_frame, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_end_date.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # added a button to open date picker for start date
        self.btn_pick_end = ctk.CTkButton(self.end_date_frame, text="📅", width=35, command=lambda: self.open_date_picker(self.entry_end_date))
        self.btn_pick_end.pack(side="right")
        
        # member entry box and "add" button
        self.lbl_member = ctk.CTkLabel(self.root, text="Member Name:")
        self.lbl_member.grid(row=5, column=0, padx=15, pady=6, sticky="e")
        
        self.member_input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.member_input_frame.grid(row=5, column=1, padx=15, pady=6, sticky="ew")
        
        self.entry_member_name = ctk.CTkEntry(self.member_input_frame, placeholder_text="2 to 20 chars", justify="center")
        self.entry_member_name.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_add_member = ctk.CTkButton(self.member_input_frame, text="Add", width=60, command=self.add_member)
        self.btn_add_member.pack(side="right")
        
        # scrollable frame to list all added members
        self.lbl_added_members = ctk.CTkLabel(self.root, text="Added Members:")
        self.lbl_added_members.grid(row=6, column=0, padx=15, pady=6, sticky="ne")
        
        self.scrollable_member_frame = ctk.CTkScrollableFrame(self.root, height=100, label_text="Group Members")
        self.scrollable_member_frame.grid(row=6, column=1, padx=15, pady=6, sticky="nsew")
        
        # Theme Switch Frame
        self.theme_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.theme_frame.grid(row=7, column=0, columnspan=2, padx=15, pady=4)
        self.theme_switch = ctk.CTkSwitch(self.theme_frame, text="Light/Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack()
        
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

        self.action_btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.action_btn_frame.grid(row=8, column=0, columnspan=2, pady=(10, 15))
        
        if self.mode == "manage_members" or self.mode == "edit_trip_details":
            btn_confirm_text = "Save"
        else:
            btn_confirm_text = "Create"
            
        self.btn_back = ctk.CTkButton(self.action_btn_frame, text="Back", fg_color="grey", hover_color="#555555", width=80, command=self.back_btn_on_click)
        self.btn_back.pack(side="left", padx=5)

        self.btn_reset = ctk.CTkButton(self.action_btn_frame, text="Reset", fg_color="#FF9500", hover_color="#CC7600", width=80, command=self.reset_form)
        self.btn_reset.pack(side="left", padx=5)
        
        self.btn_create = ctk.CTkButton(self.action_btn_frame, text=btn_confirm_text, fg_color="#0080FF", width=90, command=self.create_btn_on_click)
        self.btn_create.pack(side="right", padx=5)
        
        if (self.mode == "manage_members" or self.mode == "edit_trip_details") and len(self.trip_info_dict) > 0:
            self.entry_trip_name.insert(0, self.trip_info_dict.get("name", ""))
            self.option_currency.set(self.trip_info_dict.get("base_currency", "NZD"))
            self.entry_start_date.insert(0, self.trip_info_dict.get("start_date", ""))
            self.entry_end_date.insert(0, self.trip_info_dict.get("end_date", ""))
            
            if self.mode == "manage_members":
                self.entry_trip_name.configure(state="disabled")
                self.option_currency.configure(state="disabled")
                self.entry_start_date.configure(state="disabled")
                self.entry_end_date.configure(state="disabled")
            
        self.update_member_list()

    def open_date_picker(self, target_entry):
        '''IMPROVEMENT: DatePicker popup window with text fallback'''
        if HAS_TKCALENDAR == True:
            picker_top = ctk.CTkToplevel(self.root)
            picker_top.title("Select Date")
            picker_top.geometry("280x250")
            picker_top.lift()
            picker_top.grab_set()
            
            cal = DateEntry(picker_top, date_pattern="dd/mm/yyyy")
            cal.pack(padx=20, pady=20)
            
            def set_date_val():
                target_entry.delete(0, "end")
                target_entry.insert(0, cal.get_date().strftime("%d/%m/%Y"))
                picker_top.destroy()
                
            btn_ok = ctk.CTkButton(picker_top, text="Select", command=set_date_val)
            btn_ok.pack(pady=10)
        else:
            messagebox.showinfo("Notice", "tkcalendar extension not installed. Please type date in dd/mm/yyyy format.", parent=self.root)

    def reset_form(self):
        '''IMPROVEMENT: Reset button function clears all entry boxes'''
        self.entry_trip_name.delete(0, "end")
        self.entry_start_date.delete(0, "end")
        self.entry_end_date.delete(0, "end")
        self.entry_member_name.delete(0, "end")
        self.option_currency.set("NZD")
        
        if self.mode != "manage_members":
            self.added_members = []
            self.update_member_list()

    def toggle_theme(self):
        '''Toggles Light/Dark mode globally'''
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def show_error(self, message):
        '''Display error message when invalid input'''
        messagebox.showerror("Error", message, parent=self.root)
        
    def add_member(self):
        '''Add a new member to the list with length range validation'''
        input_name = self.entry_member_name.get().strip()

        if input_name == "":
            self.show_error("Member name cannot be blank!")
            return
            
        # Added a member name range validation (2 to 20 characters)
        if len(input_name) < 2 or len(input_name) > 20:
            self.show_error("Member name length must be between 2 and 20 characters!")
            return

        if re.match(r"^[A-Za-z0-9\s]+$", input_name) == None:
            self.show_error("Member name can only contain letters and numbers!")
            return
            
        existing_lower = []
        for member_item in self.added_members:
            existing_lower.append(member_item.lower())
            
        if input_name.lower() in existing_lower:
            self.show_error("Member is already added!")
            return
        
        self.added_members.append(input_name)
        self.entry_member_name.delete(0, "end")
        self.update_member_list()
        
    def remove_member(self, name):
        '''Remove a member from the list'''
        if name in self.added_members:
            self.added_members.remove(name)
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
            
            def make_delete_cmd(target_name):
                return lambda: self.remove_member(target_name)
                
            btn_remove = ctk.CTkButton(member_list, text="X", width=25, height=20, fg_color="#FF4D4D", hover_color="#CC0000", command=make_delete_cmd(name))
            btn_remove.pack(side="right", padx=5)
            
            self.memeber_list_widgets.append(member_list)

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
        if self.mode == "create_trip":
            if self.validate_input() == False:
                return
            
            trip_name = self.entry_trip_name.get().strip()
            
            if os.path.exists(self.folder_path) == False:
                os.makedirs(self.folder_path)
            
            clean_file_name = trip_name.lower().replace(" ", "_") + ".json"
            file_path = os.path.join(self.folder_path, clean_file_name)
            
            if os.path.exists(file_path) == True:
                confirm = messagebox.askyesno("Overwrite Warning", f"A trip named '{trip_name}' already exists!\nDo you want to overwrite it?", parent=self.root)
                if confirm == False:
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
                messagebox.showinfo("Success", f"Trip '{trip_name}', successfully created", parent=self.root)

                if self.on_trip_created_callback:
                    self.on_trip_created_callback(file_path)
            except FileNotFoundError:
                self.show_error(f"Could not save the trip: {file_path}")
                
        elif self.mode == "manage_members" or self.mode == "edit_trip_details":
            if len(self.added_members) == 0:
                self.show_error("You must have at least 1 member in the trip!")
                return
                
            if self.file_path == None:
                self.show_error("No trip file provided to update!")
                return

            self.trip_info_dict["name"] = self.entry_trip_name.get().strip()
            self.trip_info_dict["base_currency"] = self.option_currency.get()
            self.trip_info_dict["start_date"] = self.entry_start_date.get().strip()
            self.trip_info_dict["end_date"] = self.entry_end_date.get().strip()
            self.trip_info_dict["members"] = self.added_members

            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(self.trip_info_dict, f, indent=4)
                messagebox.showinfo("Success", "Trip details updated successfully!", parent=self.root)
                
                if self.on_trip_created_callback:
                    self.on_trip_created_callback(self.file_path)
            except FileNotFoundError:
                self.show_error(f"Could not find trip file to update: {self.file_path}")

    def back_btn_on_click(self):
        '''Return to the launcher or dashboard window'''
        if self.on_back_callback:
            self.on_back_callback()
        else:
            print("Back button clicked")
