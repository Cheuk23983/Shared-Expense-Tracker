# Purpose: This part of the component is to display detail of a chosen trip on the launcher, like the transactions, settlement, and member balance etc.
# Author: Hubert Kwan
# Date: 04/08/2026
# Version: 1.0


# import libraries and modules
import os
import json
from datetime import datetime
import fontawesome as fa
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
        self.lower_split_frame = ctk.CTkFrame(self.middle_frame, fg_color="transparent")
        self.lower_split_frame.grid(row=1, column=0, sticky="nsew")
        # column for member balance
        self.lower_split_frame.grid_columnconfigure(0, weight=1)
        # coloumn for expense table
        self.lower_split_frame.grid_columnconfigure(1, weight=2)
        self.lower_split_frame.grid_rowconfigure(0, weight=1)
        
        # Member balance box
        self.member_balance_box = ctk.CTkFrame(self.lower_split_frame, corner_radius=10)
        self.member_balance_box.grid(row=0, column=0, padx=(0,10), sticky="nsew")
        # member balance title
        self.lbl_balance_title = ctk.CTkLabel(self.member_balance_box, text="Member Balances", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_balance_title.pack(pady=10)
        #scrollable frame to show all member
        self.member_scrollable_box = ctk.CTkScrollableFrame(self.member_balance_box, fg_color="transparent")
        self.member_scrollable_box.pack(fill="both", expand=True, padx=5, pady=5)
        # button to manage members (add/remove)
        self.btn_manage_member = ctk.CTkButton(self.member_scrollable_box, text="Add/Remove member", height=30)
        self.btn_manage_member.pack(padx=10)
        
        self.table_container_frame = ctk.CTkFrame(self.lower_split_frame, fg_color="transparent")
        self.table_container_frame.grid(row=0, column=1, sticky="nsew")
        self.table_container_frame.grid_columnconfigure(0, weight=1)
        self.table_container_frame.grid_rowconfigure(1, weight=1)
        
        self.table_header_frame = ctk.CTkFrame(self.table_container_frame, height=35, fg_color="#adadad")
        self.table_header_frame.grid(row=0, column=0, sticky="ew", pady=(0,5))
        self.table_header_frame.grid_columnconfigure(0, weight=2)
        self.table_header_frame.grid_columnconfigure(1, weight=3)
        self.table_header_frame.grid_columnconfigure(2, weight=2)
        self.table_header_frame.grid_columnconfigure(3, weight=2)
        self.table_header_frame.grid_columnconfigure(4, weight=2)
        self.table_header_frame.grid_columnconfigure(5, weight=2)
        
        lbl_header_date = ctk.CTkLabel(self.table_header_frame, text="Date", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_date.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        lbl_header_description = ctk.CTkLabel(self.table_header_frame, text="Description", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_description.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        lbl_header_category = ctk.CTkLabel(self.table_header_frame, text="Category", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_category.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        lbl_header_payer = ctk.CTkLabel(self.table_header_frame, text="Payer", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_payer.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        lbl_header_amount = ctk.CTkLabel(self.table_header_frame, text="Amount", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_amount.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        
        lbl_header_action = ctk.CTkLabel(self.table_header_frame, text="Action", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_action.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        
        self.transactions_scrollable_frame = ctk.CTkScrollableFrame(self.table_container_frame)
        self.transactions_scrollable_frame.grid(row=1, column=0, sticky="nsew")
        self.transactions_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.btn_add_expense = ctk.CTkButton(self.right_frame, text="+ Add Expense", fg_color="#0080ff", height=35)
        self.btn_add_expense.pack(fill="x", pady=(0, 8))
        
        self.btn_save_changes = ctk.CTkButton(self.right_frame, text="✔ Save Changes", fg_color="#00a86b", height=35)
        self.btn_save_changes.pack(fill="x", pady=(0, 15))
        
        self.settlement_box = ctk.CTkFrame(self.right_frame, corner_radius=10)
        self.settlement_box.pack(fill="both", expand=True)

        self.lbl_settle_title = ctk.CTkLabel(
            self.settlement_box, 
            text="Simplified Settlement", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_settle_title.pack(pady=10)

        self.settlements_scroll_box = ctk.CTkScrollableFrame(self.settlement_box, fg_color="transparent")
        self.settlements_scroll_box.pack(fill="both", expand=True, padx=5, pady=5)

        # self.refresh_dashboard()
        
    def refresh_dashboard(self):
        '''refresh money details, transaction table, member balance, and settlement'''
        # get trip data from json file
        expenses_list = self.trip_info_dict.get("expenses", [])
        currency = self.trip_info_dict.get("base_currency", "NZD")
        group_members = self.trip_info_dict.get("members", [])
        
root = ctk.CTk()
app = TripDashboard(root)
root.mainloop()

        
        

