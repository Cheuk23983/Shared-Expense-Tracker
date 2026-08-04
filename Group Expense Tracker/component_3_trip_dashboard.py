# Purpose: This part of the component is to display detail of a chosen trip on the launcher, like the transactions, settlement, and member balance etc.
# Author: Hubert Kwan
# Date: 04/08/2026
# Version: 1.0


# import libraries and modules
import os
import json
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox


class TripDashboard:
    def __init__(self, root, file_path=None):
        self.root = root
        self.root.title("Trip Dashboard")
        self.root.geometry("1050x850")
        
        self.file_path = file_path
        self.trip_info_dict = {}
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # self.load_trip_file()
        
        self.create_widgets()
        
    
    # def load_trip_file(self):
    #     '''load a trip json data from a file'''
    #     with open(self.file_path, "r", encoding="utf-8") as file_data:
    #         self.trip_info_dict = json.load(file_data)


    def create_widgets(self):
        '''creates trip dashbaord layout'''
        # top title frame (trip name & reutrn button)
        self.top_title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_title_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")
        # trip name label
        trip_name = self.trip_info_dict.get("name", "Trip Dashboard")
        self.lbl_trip_title = ctk.CTkLabel(self.top_title_frame, text=f"Trip: {trip_name}", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_trip_title.pack(side="left")
        # retrun button
        self.btn_back = ctk.CTkButton(self.top_title_frame, text="Back", width=80, fg_color="gray", hover_color="#555555")
        self.btn_back.pack(side="right")
        
        # main frame (member balance, transaction detail, and settlement)
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, padx=20, pady=(15, 5), sticky="ew")
        # member balance & the transaction detail
        self.main_frame.grid_columnconfigure(0, weight=1)
        # settlement & function button
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        #
        self.middle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.middle_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(1, weight=1)
        
        # frame to hold the total cost
        self.total_cost_box = ctk.CTkFrame(self.middle_frame, height=50, corner_radius=8)
        self.total_cost_box.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        # label of the total cost
        self.lbl_total_cost = ctk.CTkLabel(self.total_cost_box, text="Total Cost: $0.00", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_total_cost.pack(side="left", padx=15, pady=10)
        
        # frame to hold the member balance and expenses table
        self.lower_split_frame = ctk.CTkFrame(self.middle_frame, fg_color="transaprent")
        self.lower_split_frame.grid(row=1, column=0, sticky="nsew")
        # column for member balance
        self.lower_split_frame.grid_columnconfigure(0, weight=1)
        # coloumn for expense table
        self.lower_split_frame.grid_columnconfigure(1, weight=2)
        self.lower_split_frame.grid_rowconfigure(0, weight=1)
        
    
    
root = ctk.CTk()
app = TripDashboard(root)
root.mainloop()

        
        

