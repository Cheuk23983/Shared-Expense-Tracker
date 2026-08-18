# Purpose: This program is the first component of the tracker project. The Component included function to manage trips. 
# Author: Hubert Kwan
# Date: 18/08/2026
# Version: 1.3

# This version  fixed bugs and error occurs when connecting to the main program

# import customtkinter module
import customtkinter as ctk
import json
import os
from tkinter import messagebox

# Set global default appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# launcher class
class MainMenuFrame:
    '''Launcher window for the tracker'''
    def __init__(self, root):
        self.root = root
        self.root.title("Group Expense Tracker")
        self.root.geometry("450x550")

        self.folder_path = "trips"
        self.trip_cards_list = []
        
        self.delete_mode_on = False
        self.on_open_trip_callback = None
        self.on_new_trip_callback = None
        
        # config frame grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        # make the GUI widgets
        self.create_widgets()
        
    def create_widgets(self):
        '''Create all widgets need for the window.'''
        # Title of the window
        self.title_label = ctk.CTkLabel(self.root, text="Group Expense Tracker", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Frame for top buttons
        self.top_buttons_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_buttons_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        # select button
        self.select_mode_btn = ctk.CTkButton(self.top_buttons_frame, text="Select", width=80, command=self.toggle_delete_mode)
        self.select_mode_btn.pack(side="left")
        
        # add trip button
        self.new_trip_btn = ctk.CTkButton(self.top_buttons_frame, text="+ New Trip", fg_color="#0080FF", command=self.create_trip_click)
        self.new_trip_btn.pack(side="right")
        
        # Frame for saved trips
        self.trip_scroll_frame = ctk.CTkScrollableFrame(self.root, label_text="Saved Trips")
        self.trip_scroll_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
    
        self.bottom_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.bottom_frame.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")
        
        self.theme_switch = ctk.CTkSwitch(self.bottom_frame, text="Light/Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="left")

        # Load data on startup
        self.load_and_display_trip()
        
    def toggle_delete_mode(self):
        if self.delete_mode_on == False:
            self.delete_mode_on = True
            self.select_mode_btn.configure(text="Cancel", fg_color="gray", hover_color="#555555")
        else:
            self.delete_mode_on = False
            self.select_mode_btn.configure(text="Select", fg_color="#1F6AA5", hover_color="#144870")
            
        self.load_and_display_trip()
            
    def delete_trip_file(self, file_path, trip_name):
        user_choice = messagebox.askyesno("Delete Trip", f"Are you sure you want to delete '{trip_name}'?\n This cannot be undone.")
        
        if user_choice == True:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    messagebox.showinfo("Success", f"'{trip_name}' has been deleted.")
                    self.load_and_display_trip()
            except FileNotFoundError:
                messagebox.showerror("Error", f"Could not delete file: {file_path}")
        
    def create_trip_click(self):
        if self.on_new_trip_callback:
            self.on_new_trip_callback()
        else:
            print("trip creation window not found.")
    
    def open_trip_click(self, file_path):
        if self.on_open_trip_callback:
            self.on_open_trip_callback(file_path)
        else:
            print(f"Trip {file_path} not found...")
        
    def load_and_display_trip(self):
        for widget in self.trip_cards_list:
            widget.destroy()
        self.trip_cards_list = []

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            
        trips_file = [
            os.path.join(self.folder_path, file)
            for file in os.listdir(self.folder_path)
            if file.endswith(".json")
        ]
        
        # show warning label if no files exist
        if len(trips_file) == 0:
            self.no_data_lbl = ctk.CTkLabel(self.trip_scroll_frame, text="No saved trips found. Click '+ New Trip' to create one")
            self.no_data_lbl.pack(pady=20)
            self.trip_cards_list.append(self.no_data_lbl)
            return
        
        # Loop through each json file found
        for trip in trips_file:
            try:
                with open(trip, "r", encoding="utf-8") as f:
                    trip_data = json.load(f)
            except Exception:
                messagebox.showerror("Error", f"Could not read file {trip}")
                continue
            
            trip_name = trip_data.get("name", "Unnamed Trip")
            currency = trip_data.get("base_currency", "NZD")
            start_date = trip_data.get("start_date", "N/A")
            end_date = trip_data.get("end_date","N/A")

            def open_cmd(path):
                return lambda: self.open_trip_click(path)
            click_command = open_cmd(trip)
            
            def delete_cmd(path, name):
                return lambda: self.delete_trip_file(path, name)

            card = ctk.CTkFrame(self.trip_scroll_frame, corner_radius=8)
            card.pack(fill="x", pady=6, padx=5)
            
            lbl_card_title = ctk.CTkLabel(card, text=trip_name, font=ctk.CTkFont(size=15, weight="bold"))
            lbl_card_title.pack(anchor="w", padx=12, pady=(8, 2))
            
            lbl_card_details = ctk.CTkLabel(card, text=f"Currency: {currency} | {start_date} to {end_date}", text_color="gray", font=ctk.CTkFont(size=11))
            lbl_card_details.pack(anchor="w", padx=12, pady=(0, 8))
            
            if self.delete_mode_on == True:
                delete_btn = ctk.CTkButton(card, text="Delete", width=70, height=28, fg_color="#FF4D4D", hover_color="#CC0000", command=delete_cmd(trip, trip_name))
                delete_btn.pack(side="right", padx=12, pady=(0, 8))
            else:
                btn_open = ctk.CTkButton(card, text="Open Trip", width=80, height= 28, command=click_command)
                btn_open.pack(side="right", padx=12, pady=(0, 8))
            
            self.trip_cards_list.append(card)

    def toggle_theme(self):
        '''Toggles Light/Dark mode'''
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

