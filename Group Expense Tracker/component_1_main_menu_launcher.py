# Purpose: This component is the program whcich creates eidgets and handle the logic for launcher window.
# Users can delete, create, and open a trip in this window. They can also change their prefered appearance mode. 
# Author: Hubert Kwan
# Date: 20/08/2026
# Version: 2.1 


# Import required libraries and modules
import customtkinter as ctk
import json
import os
from tkinter import messagebox

# Constants
DEFAULT_TRIPS_FOLDER = "trips"
DEFAULT_CURRENCY = "NZD"

# UI Theme Color Constants
COLOR_NEW_TRIP_BTN = "#0080FF"
COLOR_SELECT_ACTIVE_BTN = "gray"
COLOR_SELECT_HOVER_BTN = "#555555"
COLOR_SELECT_DEFAULT_BTN = "#1F6AA5"
COLOR_SELECT_DEFAULT_HOVER_BTN = "#144870"
COLOR_DELETE_BTN = "#FF4D4D"
COLOR_DELETE_HOVER_BTN = "#CC0000"

# Set global default appearance mode to follow system settings and set the default blue theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Main launcher class that acts as the home screen showing all saved trips
class MainMenuFrame:
    '''Launcher window for the tracker'''
    def __init__(self, root):
        self.root = root
        self.root.title("Group Expense Tracker")
        self.root.geometry("450x550")

        # Define default folder name where saved trip JSON files will be stored
        self.folder_path = DEFAULT_TRIPS_FOLDER
        self.trip_cards_list = []
        
        # Flag fot delete mode and callback function
        self.delete_mode_on = False
        self.on_open_trip_callback = None
        self.on_new_trip_callback = None
        
        # Configure grid column and row to be responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        # Call function to build all the GUI
        self.create_widgets()
        
    def create_widgets(self):
        '''Create all widgets need for the window.'''
        # Display header label
        self.title_label = ctk.CTkLabel(self.root, text="Group Expense Tracker", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Top action frame holding select/delete mode and new trip creation buttons
        self.top_buttons_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_buttons_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        # Button to toggle select/delete mode on or off
        self.select_mode_btn = ctk.CTkButton(self.top_buttons_frame, text="Select", width=80, command=self.toggle_delete_mode)
        self.select_mode_btn.pack(side="left")
        
        # Button to trigger the creation of a new trip file
        self.new_trip_btn = ctk.CTkButton(self.top_buttons_frame, text="+ New Trip", fg_color=COLOR_NEW_TRIP_BTN, command=self.create_trip_click)
        self.new_trip_btn.pack(side="right")
        
        # Scrollable frame container that will display all created trip cards
        self.trip_scroll_frame = ctk.CTkScrollableFrame(self.root, label_text="Saved Trips")
        self.trip_scroll_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
    
        # Bottom frame container reserved for global controls like the light/dark mode switch
        self.bottom_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.bottom_frame.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")
        
        # Switch widget to allow toggling between Light and Dark mode
        self.theme_switch = ctk.CTkSwitch(self.bottom_frame, text="Light/Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="left")
        
        # Match switch state with the current system appearance mode on startup
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

        # Load existing JSON files from the folder and display them as cards on screen startup
        self.load_and_display_trip()
        
    def toggle_delete_mode(self):
        # Toggles delete mode flag and updates button appearance
        if self.delete_mode_on == False:
            self.delete_mode_on = True
            self.select_mode_btn.configure(text="Cancel", fg_color=COLOR_SELECT_ACTIVE_BTN, hover_color=COLOR_SELECT_HOVER_BTN)
        else:
            self.delete_mode_on = False
            self.select_mode_btn.configure(text="Select", fg_color=COLOR_SELECT_DEFAULT_BTN, hover_color=COLOR_SELECT_DEFAULT_HOVER_BTN)
            
        # Refresh trip cards list view to update action button states
        self.load_and_display_trip()
            
    def delete_trip_file(self, file_path, trip_name):
        # Ask user for confirmation before permanently deleting a JSON trip file
        user_choice = messagebox.askyesno("Delete Trip", f"Are you sure you want to delete '{trip_name}'?\n This cannot be undone.")
        
        if user_choice == True:
            try:
                # Remove file from disk and reload the launcher card list
                if os.path.exists(file_path):
                    os.remove(file_path)
                    messagebox.showinfo("Success", f"'{trip_name}' has been deleted.")
                    self.load_and_display_trip()
            except FileNotFoundError:
                messagebox.showerror("Error", f"Could not delete file: {file_path}")
        
    def create_trip_click(self):
        # Trigger callback function assigned by controller to transition to creation screen
        if self.on_new_trip_callback:
            self.on_new_trip_callback()
        else:
            print("trip creation window not found.")
    
    def open_trip_click(self, file_path):
        # Trigger callback function assigned by controller to open dashboard for selected file
        if self.on_open_trip_callback:
            self.on_open_trip_callback(file_path)
        else:
            print(f"Trip {file_path} not found...")
        
    def load_and_display_trip(self):
        # Clear out previous card widgets from list before re-rendering
        for widget in self.trip_cards_list:
            widget.destroy()
        self.trip_cards_list = []

        # Create trips directory if it does not exist yet
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            
        # Get list of all valid JSON trip files inside folder
        trips_file = [
            os.path.join(self.folder_path, file)
            for file in os.listdir(self.folder_path)
            if file.endswith(".json")
        ]
        
        # Display warning label if no saved trips were found in the folder
        if len(trips_file) == 0:
            self.no_data_lbl = ctk.CTkLabel(self.trip_scroll_frame, text="No saved trips found. Click '+ New Trip' to create one")
            self.no_data_lbl.pack(pady=20)
            self.trip_cards_list.append(self.no_data_lbl)
            return
        
        # Loop through each JSON file, read trip data, and build card widgets
        for trip in trips_file:
            try:
                with open(trip, "r", encoding="utf-8") as f:
                    trip_data = json.load(f)
            except FileNotFoundError:
                messagebox.showerror("Error", f"Could not find file {trip}")
                continue
            
            # Extract trip dadta safely with fallback default strings
            trip_name = trip_data.get("name", "Unnamed Trip")
            currency = trip_data.get("base_currency", DEFAULT_CURRENCY)
            start_date = trip_data.get("start_date", "N/A")
            end_date = trip_data.get("end_date","N/A")

            def open_cmd(path):
                return lambda: self.open_trip_click(path)
            click_command = open_cmd(trip)
            
            def delete_cmd(path, name):
                return lambda: self.delete_trip_file(path, name)

            # Build individual card container frame for each trip
            card = ctk.CTkFrame(self.trip_scroll_frame, corner_radius=8)
            card.pack(fill="x", pady=6, padx=5)
            
            # Label displaying trip title inside card
            lbl_card_title = ctk.CTkLabel(card, text=trip_name, font=ctk.CTkFont(size=15, weight="bold"))
            lbl_card_title.pack(anchor="w", padx=12, pady=(8, 2))
            
            # Label displaying currency and date range summary
            lbl_card_details = ctk.CTkLabel(card, text=f"Currency: {currency} | {start_date} to {end_date}", text_color="gray", font=ctk.CTkFont(size=11))
            lbl_card_details.pack(anchor="w", padx=12, pady=(0, 8))
            
            # Display either a Delete button or an Open Trip button depending on mode state
            if self.delete_mode_on == True:
                delete_btn = ctk.CTkButton(card, text="Delete", width=70, height=28, fg_color=COLOR_DELETE_BTN, hover_color=COLOR_DELETE_HOVER_BTN, command=delete_cmd(trip, trip_name))
                delete_btn.pack(side="right", padx=12, pady=(0, 8))
            else:
                btn_open = ctk.CTkButton(card, text="Open Trip", width=80, height= 28, command=click_command)
                btn_open.pack(side="right", padx=12, pady=(0, 8))
            
            # Track created widget in local list
            self.trip_cards_list.append(card)

    def toggle_theme(self):
        '''Toggles Light/Dark mode'''
        # Switch overall the theme based on toggle switch position
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
