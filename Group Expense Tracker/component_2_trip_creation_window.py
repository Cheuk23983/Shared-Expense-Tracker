# Purpose: Component 2 is the trip creation window. This windows allow users to enter all details for the trip.
# Users could enter the trip title, currency, trip period, and member names effortlessly.
# Date: 20/08/2026
# Version: 2.1

# Imporvements:
# 1. Date picker has changed with a better layout. Instead of clicking mutliple buttons to open ther date pciker after pressed the calendar icon, it now shows up instantly.
# 2. Fixed row gaps. 

# Import required libraries and modules
import os
import json
import re
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

# Logic Constants
DEFAULT_TRIPS_FOLDER = "trips"
DEFAULT_CURRENCY = "NZD"
MIN_MEMBER_NAME_LENGTH = 2
MAX_MEMBER_NAME_LENGTH = 20

# UI Theme Color Constants
COLOR_PRIMARY_BLUE = "#0080FF"
COLOR_RESET_BTN = "#FF9500"
COLOR_RESET_HOVER_BTN = "#CC7600"
COLOR_BACK_BTN = "grey"
COLOR_BACK_HOVER_BTN = "#555555"
COLOR_REMOVE_BTN = "#FF4D4D"
COLOR_REMOVE_HOVER_BTN = "#CC0000"
COLOR_DISABLED_BTN = "gray"

# Expanded World Currencies List Constant
CURRENCY_LIST = [
    "NZD", "AUD", "USD", "EUR", "GBP", "JPY", "CAD", "CHF", "CNY", "HKD",
    "SGD", "KRW", "INR", "THB", "MYR", "IDR", "PHP", "VND", "TWD", "MXN",
    "BRL", "ZAR", "NOK", "SEK", "DKK", "PLN", "AED", "SAR", "EGP", "FJD"
]

# Optional datepicker extension for user
try:
    from tkcalendar import Calendar
    HAS_TKCALENDAR = True
except ImportError:
    HAS_TKCALENDAR = False

# Set global appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class TripCreationWindow:
    '''Class to create or manage trip details and group members'''

    def __init__(self, root, mode="create_trip", file_path=None):
        # Store window state variables and operating mode
        self.root = root
        self.mode = mode
        self.file_path = file_path
        self.trip_info_dict = {}

        # set title based on current screen operating mode
        if self.mode == "manage_members":
            self.root.title("Manage Trip Members")
        elif self.mode == "edit_trip_details":
            self.root.title("Edit Trip Details")
        else:
            self.root.title("Trip Creation Window")
        self.root.geometry("480x680")

        # Initialize default variables for storage path and member lists
        self.folder_path = DEFAULT_TRIPS_FOLDER
        self.added_members = []
        self.memeber_list_widgets = []

        # main program callback function
        self.on_back_callback = None
        self.on_trip_created_callback = None

        # Pre-load existing data from JSON if running in edit or manage members mode
        if (self.mode == "manage_members" or self.mode == "edit_trip_details") and self.file_path != None and os.path.exists(self.file_path):
            self.load_existing_trip_data()

        # Build form inputs and GUI layout
        self.create_widgets()

    def load_existing_trip_data(self):
        '''Loads existing trip details from the JSON file'''
        if self.file_path == None:
            return
        try:
            # Read JSON file into memory and extract member list
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.trip_info_dict = json.load(f)
                self.added_members = list(self.trip_info_dict.get("members", []))
        except FileNotFoundError:
            self.show_error(f"Could not find file: {self.file_path}")

    def open_date_picker(self, target_entry):
        '''Opens full calendar pop-up directly on top layer with explicit visible text colors'''
        if HAS_TKCALENDAR == True:
            # Create a modal pop-up window containing the calendar widget
            picker_top = ctk.CTkToplevel(self.root)
            picker_top.title("Select Date")
            picker_top.geometry("320x300")
            picker_top.resizable(False, False)

            # Ensure popup stays on top and focuses user interaction
            picker_top.transient(self.root)
            picker_top.lift()
            picker_top.focus_force()
            picker_top.grab_set()

            # Calendar widget with custom colors for visibility
            cal = Calendar(
                picker_top,
                selectmode="day",
                date_pattern="dd/mm/yyyy",
                cursor="hand2",
                headersforeground="#333333",
                selectforeground="#FFFFFF",
                normalforeground="#000000",
                weekendforeground="#000000"
            )
            cal.pack(padx=15, pady=15, fill="both", expand=True)

            # function to copy selected date string into entry box
            def set_date_val():
                selected_date_str = cal.get_date()
                target_entry.delete(0, "end")
                target_entry.insert(0, selected_date_str)
                picker_top.grab_release()
                picker_top.destroy()

            # Confirm button to check the calendar pick
            btn_ok = ctk.CTkButton(picker_top, text="Confirm Date", fg_color=COLOR_PRIMARY_BLUE, command=set_date_val)
            btn_ok.pack(pady=(0, 12))
        else:
            # Fallback message if tkcalendar library is not installed
            messagebox.showinfo("Notice", "tkcalendar extension not installed. Please type date in dd/mm/yyyy format.", parent=self.root)

    def reset_form(self):
        '''Resets input fields only when creating a new trip; blocked in manage/edit modes'''
        if self.mode in ["manage_members", "edit_trip_details"]:
            return

        # Clear all input entry fields and reset dropdown default
        self.entry_trip_name.delete(0, "end")
        self.entry_start_date.delete(0, "end")
        self.entry_end_date.delete(0, "end")
        self.entry_member_name.delete(0, "end")
        self.option_currency.set(DEFAULT_CURRENCY)
        self.added_members = []
        self.update_member_list()

    def toggle_theme(self):
        '''Toggles Light/Dark mode globally'''
        # Switch appearance mode based on toggle position
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def create_widgets(self):
        '''Builds layout inside main container'''
        # Create container frame to center content
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=15)

        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)

        # display header text based on mode
        if self.mode == "manage_members":
            heading_text = "Manage Trip Members"
        elif self.mode == "edit_trip_details":
            heading_text = "Edit Trip Details"
        else:
            heading_text = "Create a Trip"

        self.lbl_title = ctk.CTkLabel(self.main_container, text=heading_text, font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.grid(row=0, column=0, columnspan=2, pady=(5, 12))

        # Trip Name input label and entry box
        self.lbl_trip_name = ctk.CTkLabel(self.main_container, text="Trip Name:")
        self.lbl_trip_name.grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.entry_trip_name = ctk.CTkEntry(self.main_container, placeholder_text="e.g. Queenstown trip", justify="center")
        self.entry_trip_name.grid(row=1, column=1, padx=10, pady=6, sticky="ew")

        # Base Currency option menu with expanded currency choices
        self.lbl_currency = ctk.CTkLabel(self.main_container, text="Base Currency:")
        self.lbl_currency.grid(row=2, column=0, padx=10, pady=6, sticky="e")
        
        self.option_currency = ctk.CTkOptionMenu(self.main_container, values=CURRENCY_LIST, width=130)
        self.option_currency.grid(row=2, column=1, padx=10, pady=6, sticky="w")

        # Start Date input field with attached calendar button
        self.lbl_start_date = ctk.CTkLabel(self.main_container, text="Start Date:")
        self.lbl_start_date.grid(row=3, column=0, padx=10, pady=6, sticky="e")

        self.start_date_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.start_date_frame.grid(row=3, column=1, padx=10, pady=6, sticky="ew")

        self.entry_start_date = ctk.CTkEntry(self.start_date_frame, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_start_date.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_picker_start = ctk.CTkButton(self.start_date_frame, text="📅", width=35, fg_color=COLOR_PRIMARY_BLUE, command=lambda: self.open_date_picker(self.entry_start_date))
        self.btn_picker_start.pack(side="right")

        # End Date input field with attached calendar button
        self.lbl_end_date = ctk.CTkLabel(self.main_container, text="End Date:")
        self.lbl_end_date.grid(row=4, column=0, padx=10, pady=6, sticky="e")

        self.end_date_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.end_date_frame.grid(row=4, column=1, padx=10, pady=6, sticky="ew")

        self.entry_end_date = ctk.CTkEntry(self.end_date_frame, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_end_date.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_picker_end = ctk.CTkButton(self.end_date_frame, text="📅", width=35, fg_color=COLOR_PRIMARY_BLUE, command=lambda: self.open_date_picker(self.entry_end_date))
        self.btn_picker_end.pack(side="right")

        # Member Name input section
        self.lbl_member = ctk.CTkLabel(self.main_container, text="Member Name:")
        self.lbl_member.grid(row=5, column=0, padx=10, pady=6, sticky="e")

        self.member_input_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.member_input_frame.grid(row=5, column=1, padx=10, pady=6, sticky="ew")

        self.entry_member_name = ctk.CTkEntry(self.member_input_frame, placeholder_text=f"{MIN_MEMBER_NAME_LENGTH} to {MAX_MEMBER_NAME_LENGTH} chars", justify="center")
        self.entry_member_name.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_add_member = ctk.CTkButton(self.member_input_frame, text="Add", width=60, command=self.add_member)
        self.btn_add_member.pack(side="right")

        # Scrollable list displaying all added trip group members
        self.lbl_added_members = ctk.CTkLabel(self.main_container, text="Added Members:")
        self.lbl_added_members.grid(row=6, column=0, padx=10, pady=6, sticky="ne")

        self.scrollable_member_frame = ctk.CTkScrollableFrame(self.main_container, height=130, label_text="Group Members")
        self.scrollable_member_frame.grid(row=6, column=1, padx=10, pady=6, sticky="ew")

        # Theme toggle switch frame
        self.theme_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.theme_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=4)
        self.theme_switch = ctk.CTkSwitch(self.theme_frame, text="Light/Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack()

        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

        # Action buttons container frame (Back, Reset, Create/Save)
        self.action_btn_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.action_btn_frame.grid(row=8, column=0, columnspan=2, pady=(12, 5))

        btn_confirm_text = "Save" if self.mode in ["manage_members", "edit_trip_details"] else "Create"

        self.btn_back = ctk.CTkButton(self.action_btn_frame, text="Back", fg_color=COLOR_BACK_BTN, hover_color=COLOR_BACK_HOVER_BTN, width=90, command=self.back_btn_on_click)
        self.btn_back.pack(side="left", padx=5)

        self.btn_reset = ctk.CTkButton(self.action_btn_frame, text="Reset", fg_color=COLOR_RESET_BTN, hover_color=COLOR_RESET_HOVER_BTN, width=90, command=self.reset_form)
        self.btn_reset.pack(side="left", padx=5)

        # Disable reset button if editing or managing an existing trip
        if self.mode in ["manage_members", "edit_trip_details"]:
            self.btn_reset.configure(state="disabled", fg_color=COLOR_DISABLED_BTN)

        self.btn_create = ctk.CTkButton(self.action_btn_frame, text=btn_confirm_text, fg_color=COLOR_PRIMARY_BLUE, width=90, command=self.create_btn_on_click)
        self.btn_create.pack(side="right", padx=5)

        # Pre-fill form fields with existing data if editing or managing members
        if len(self.trip_info_dict) > 0:
            self.entry_trip_name.insert(0, self.trip_info_dict.get("name", ""))
            self.option_currency.set(self.trip_info_dict.get("base_currency", DEFAULT_CURRENCY))
            self.entry_start_date.insert(0, self.trip_info_dict.get("start_date", ""))
            self.entry_end_date.insert(0, self.trip_info_dict.get("end_date", ""))

            # Disable non-editable fields if only managing members
            if self.mode == "manage_members":
                self.entry_trip_name.configure(state="disabled")
                self.option_currency.configure(state="disabled")
                self.entry_start_date.configure(state="disabled")
                self.entry_end_date.configure(state="disabled")
                self.btn_picker_start.configure(state="disabled")
                self.btn_picker_end.configure(state="disabled")

        # updated members inside scroll box
        self.update_member_list()

    def show_error(self, message):
        '''Display error message popup'''
        messagebox.showerror("Error", message, parent=self.root)

    def add_member(self):
        '''Add a new member with length range and character validation'''
        input_name = self.entry_member_name.get().strip()

        # Validate blank input
        if input_name == "":
            self.show_error("Member name cannot be blank!")
            return

        # Validate name length range (2 to 20 characters)
        if len(input_name) < MIN_MEMBER_NAME_LENGTH or len(input_name) > MAX_MEMBER_NAME_LENGTH:
            self.show_error(f"Member name length must be between {MIN_MEMBER_NAME_LENGTH} and {MAX_MEMBER_NAME_LENGTH} characters!")
            return

        # Validate pattern for allowed characters (letters and spaces)
        if re.match(r"^[A-Za-z\s]+$", input_name) == None:
            self.show_error("Member name can only contain letters and space!")
            return

        # Validate duplicate member names case-insensitively
        added_member_lower = [m.lower() for m in self.added_members]
        if input_name.lower() in added_member_lower:
            self.show_error("Member is already added!")
            return

        # Append valid member and refresh list
        self.added_members.append(input_name)
        self.entry_member_name.delete(0, "end")
        self.update_member_list()

    def remove_member(self, name):
        '''Remove a member from the list'''
        if name in self.added_members:
            self.added_members.remove(name)
            self.update_member_list()

    def update_member_list(self):
        '''Update scrollable member frame'''
        # Destroy previous widget elements
        for widget in self.memeber_list_widgets:
            widget.destroy()
        self.memeber_list_widgets = []

        # Create row widget containing member name and remove button for each added person
        for name in self.added_members:
            member_list = ctk.CTkFrame(self.scrollable_member_frame, fg_color="transparent")
            member_list.pack(fill="x", pady=2)

            lbl_name = ctk.CTkLabel(member_list, text=f"{name}", font=ctk.CTkFont(size=13))
            lbl_name.pack(side="left", padx=5)

            btn_remove = ctk.CTkButton(
                member_list, text="X", width=25, height=20, fg_color=COLOR_REMOVE_BTN, hover_color=COLOR_REMOVE_HOVER_BTN,
                command=lambda target_name=name: self.remove_member(target_name)
            )
            btn_remove.pack(side="right", padx=5)
            self.memeber_list_widgets.append(member_list)

    def validate_input(self):
        '''Validate input fields before saving trip'''
        name = self.entry_trip_name.get().strip()
        start_date_str = self.entry_start_date.get().strip()
        end_date_str = self.entry_end_date.get().strip()

        # Check for blank trip name
        if name == "":
            self.show_error("Trip name cannot be blank!")
            return False

        # Check for blank dates
        if start_date_str == "" or end_date_str == "":
            self.show_error("Start date and End date cannot be blank!")
            return False

        # Verify correct date formatting and logical date ordering
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

            if end_date < start_date:
                self.show_error("End date cannot be before start date!")
                return False
        except ValueError:
            self.show_error("Dates must be in dd/mm/yyyy format!")
            return False

        # Verify that at least one group member has been added
        if len(self.added_members) == 0:
            self.show_error("You must add at least 1 member to the trip!")
            return False

        return True

    def create_btn_on_click(self):
        '''Save trip data or update existing members/details'''
        if self.mode == "create_trip":
            # Validate inputs before creating file
            if not self.validate_input():
                return

            trip_name = self.entry_trip_name.get().strip()
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)

            # Generate standardized JSON filename from trip title
            clean_file_name = trip_name.lower().replace(" ", "_") + ".json"
            file_path = os.path.join(self.folder_path, clean_file_name)

            # Warn user if overwriting an existing file
            if os.path.exists(file_path):
                confirm = messagebox.askyesno(
                    "Overwrite Warning",
                    f"A trip named '{trip_name}' already exists!\nDo you want to overwrite it?",
                    parent=self.root
                )
                if not confirm:
                    return

            # Construct data structure dictionary
            trip_data = {
                "name": trip_name,
                "base_currency": self.option_currency.get(),
                "start_date": self.entry_start_date.get().strip(),
                "end_date": self.entry_end_date.get().strip(),
                "members": self.added_members,
                "expenses": []
            }

            # Save dictionary into JSON file on disk
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(trip_data, f, indent=4)
                messagebox.showinfo("Success", f"Trip '{trip_name}' successfully created", parent=self.root)

                if self.on_trip_created_callback:
                    self.on_trip_created_callback(file_path)
            except FileNotFoundError:
                self.show_error(f"Could not save trip file: {file_path}")

        elif self.mode in ["manage_members", "edit_trip_details"]:
            # Validate member count for management modes
            if len(self.added_members) == 0:
                self.show_error("You must have at least 1 member in the trip!")
                return

            if not self.file_path:
                self.show_error("No trip file provided to update!")
                return

            # Update dictionary values
            self.trip_info_dict["name"] = self.entry_trip_name.get().strip()
            self.trip_info_dict["base_currency"] = self.option_currency.get()
            self.trip_info_dict["start_date"] = self.entry_start_date.get().strip()
            self.trip_info_dict["end_date"] = self.entry_end_date.get().strip()
            self.trip_info_dict["members"] = self.added_members

            # Save updated data back to file
            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(self.trip_info_dict, f, indent=4)
                messagebox.showinfo("Success", "Trip details updated successfully!", parent=self.root)

                if self.on_trip_created_callback:
                    self.on_trip_created_callback(self.file_path)
            except FileNotFoundError:
                self.show_error(f"Could not find trip file: {self.file_path}")

    def back_btn_on_click(self):
        '''Return to previous window'''
        if self.on_back_callback:
            self.on_back_callback()
