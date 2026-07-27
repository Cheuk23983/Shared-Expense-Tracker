# Purpose: This program is the first component of the tracker project. The Component included function to manage trips. 
# Author: Hubert Kwan
# Date: 21/07/2026
# Version: 1.0

# import customtkinter module
import customtkinter as ctk
import json
from tkinter import messagebox

# Set global default appearance mode and efault color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# launcher class
class MainMenuFrame:
    '''Launcher window for the tracker'''
    def __init__(self, root):
        self.root = root
        self.root.title("Group Expense Tracker")
        self.geometry("450x550")

        self.folder_path = "trips"
        self.trip_ui_widgets = []

        
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
        self.new_trip_btn = ctk.CTkButton(self.action_frame, text="+ New Trip", fg_color="#0080FF", command=self.create_trip)
        self.new_trip_btn.pack(side="right")
        
        # Frame for saved trips
        self.trip__scroll_frame = ctk.CTkFrame(self, label_text="saved Trips")
        self.trip__scroll_frame.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")
        
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")
        
        self.theme_switch = ctk.CTkSwitch(self.bottom_frame, text="Light/Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="left")

        # Load data on startup
        self.load_and_display_trips()
        
    
    def create_trip_click(self):
        print("Opening Creation Window...")
    
    
    def open_trip_click(self):
        print(f"Opening trip...")
        
    
    def load_and_display_trip(self):
        for widget in self.trip_ui_widgets:
            widget.destroy()
        self.trip_ui_widgets = []


        # trial for read and load json files
        # trial A
        trip_files = ["queenstown_trip.json", "japan_holiday.json"]
        
        # trial B
        import os
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            
        trips_file = [
            os.path.join(self.folder_path, file)
            for file in os.listdir(self.folder_path)
            if file.endswith(".json")
        ]
        
        # show warning label if no files exist
        if len(trips_file) == 0:
            self.no_data_lbl = ctk.CTkLabel(self.scroll_trips, text="No saved trips found. Click '+ New Trip' to create one")
            self.no_data_lbl.pack(pady=20)
            self.trip_ui_widgets.append(self.no_data_lbl)
            return
        
        # Loop through eac json file found
        for trip in trips_file:
            try:
                with open(trip, "r") as f:
                    trip_data = json.load(f)
            except FileNotFoundError:
                messagebox.showerror("Error", f"Could not read file {trip}")
                continue
            
        trip_name = trip_data.get("name", "Unnamed Trip")
        currency = trip_data.get("base_currency", "NZD")
        start_date = trip_data.get("start_date", "N/A")
        end_date = trip_data.get("end_date","N/A")


        def click_handler(path):
            return lambda: self.open_trip_click(path)
        click_command = click_handler(trip)

        # Create Trips Button Frame
        # trial 1
        # btn = ctk.CTkButton(
        #         self.trips_scroll_frame,
        #         text=trip_name,
        #         height=40,
        #         font=ctk.CTkFont(size=14),
        #         command=click_handler(trip_name)
        #     )
        # btn.pack(fill="x", pady=5, padx=5)
        # self.trip_ui_widgets.append(btn)
        
        # trial 2
        card = ctk.CTkFrame(self.scroll_trip, corner_radius=8)
        card.pack(fill="x", pady=6, padx=5)
        
        lbl_card_title = ctk.CTkLabel(card, text=trip_name, font=ctk.CTkFont(size=15, weight="bold"))
        lbl_card_title.pack(anchor="w", padx=12, pady=(8, 2))
        
        lbl_card_details = ctk.CTkLabel(card, text=f"Currency: {currency} | {start_date} to {end_date}", text_color="gray", font=ctk.CTkFont(size=11))
        lbl_card_details.pack(anchor="w", padx=12, pady=(8, 2))
        
        btn_open = ctk.CTkButton(card, text="Open Trip", width=80, height= 28, commond=click_command)
        btn_open.pack(side="right", padx=12, pady=(0, 8))
        
        self.trip_ui_widgets.append(card)

    def toggle_theme(self):
            '''Toggles Light/Dark mode'''
            if self.switch_theme.get() == 1:
                ctk.set_appearance_mode("Dark")
            else:
                ctk.set_appearance_mode("Light")


# --- Application Entry Point ---
if __name__ == "__main__":
    root = ctk.CTk()
    app = MainMenuFrame(root)

    root.mainloop()
