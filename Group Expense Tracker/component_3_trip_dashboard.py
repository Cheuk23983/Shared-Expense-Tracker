# Purpose: This part of the component is to display detail of a chosen trip on the launcher, like the transactions, settlement, and member balance etc.
# Author: Hubert Kwan
# Date: 04/08/2026
# Version: 1.0


# import libraries and modules
import os
import json
import customtkinter as ctk
from PIL import Image
from datetime import datetime
from tkinter import messagebox

# Set up app appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class TripDashboard:
    '''Main GUI window class for displaying trip summary and expense details'''
    def __init__(self, root, file_path="trips/japan.json"):
        '''Initialises the dashboard window and loads trip data'''
        self.root = root
        self.root.title("Trip Dashboard")
        self.root.geometry("1200x550")
        
        self.file_path = file_path
        self.trip_info_dict = {}

        # Load PNG button icons using PIL for action buttons
        self.delete_icon = ctk.CTkImage(
            light_image=Image.open("assets/delete.png"),
            dark_image=Image.open("assets/delete.png"),
            size=(16, 16)
        )
        self.edit_icon = ctk.CTkImage(
            light_image=Image.open("assets/edit.png"),
            dark_image=Image.open("assets/edit.png"),
            size=(16, 16)
        )
        
        # Configure main window layout weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Load trip data if file path exists on computer
        if self.file_path and os.path.exists(self.file_path):
            self.load_trip_file()
        
        # Build UI layout widgets
        self.create_widgets()
        
    def load_trip_file(self):
        '''Loads trip details safely from the selected JSON file'''
        try:
            with open(self.file_path, "r", encoding="utf-8") as file_data:
                self.trip_info_dict = json.load(file_data)
        except FileNotFoundError:
            self.show_error(f"Could not find trip file '{self.file_path}'!")

    def create_widgets(self):
        '''creates trip dashbaord layout'''
        # top title frame (trip name & reutrn button)
        self.top_title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_title_frame.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        # trip name label
        trip_name = self.trip_info_dict.get("name", "Trip Dashboard")
        self.lbl_trip_title = ctk.CTkLabel(self.top_title_frame, text=f"Trip: {trip_name}", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_trip_title.pack(side="left")
        # retrun button
        self.btn_back = ctk.CTkButton(self.top_title_frame, text="Back", width=80, fg_color="gray", hover_color="#555555", command=self.back_btn_on_click)
        self.btn_back.pack(side="right")
        
        # main frame (member balance, transaction detail, and settlement)
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")
        # 3:1 column ratio to enusre teh table section has the biggest area
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # left side column frame
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
        
        # changed from a grid layout to pack layout so the table has fixed width.
        self.table_header_frame = ctk.CTkFrame(self.table_container_frame, height=35, fg_color="#adadad")
        self.table_header_frame.grid(row=0, column=0, sticky="ew", pady=(0,5))
        
        lbl_header_date = ctk.CTkLabel(self.table_header_frame, text="Date", width=85, anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_date.pack(side="left", padx=(10, 5), pady=5)
        
        lbl_header_description = ctk.CTkLabel(self.table_header_frame, text="Description", width=160, anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_description.pack(side="left", padx=5, pady=5)
        
        lbl_header_category = ctk.CTkLabel(self.table_header_frame, text="Category", width=110, anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_category.pack(side="left", padx=5, pady=5)
        
        lbl_header_payer = ctk.CTkLabel(self.table_header_frame, text="Payer", width=75, anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_payer.pack(side="left", padx=5, pady=5)
        
        lbl_header_amount = ctk.CTkLabel(self.table_header_frame, text="Amount", width=75, anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_amount.pack(side="left", padx=5, pady=5)
        
        lbl_header_action = ctk.CTkLabel(self.table_header_frame, text="Action", width=60, anchor="center", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_header_action.pack(side="left", padx=5, pady=5)
        
        
        self.transactions_scrollable_frame = ctk.CTkScrollableFrame(self.table_container_frame)
        self.transactions_scrollable_frame.grid(row=1, column=0, sticky="nsew")
        
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.btn_add_expense = ctk.CTkButton(self.right_frame, text="+ Add Expense", fg_color="#0080ff", height=35, command=self.add_expense_btn_on_click)
        self.btn_add_expense.pack(fill="x", pady=(0, 8))
        
        self.btn_save_changes = ctk.CTkButton(self.right_frame, text="✔ Save Changes", fg_color="#00a86b", height=35, command=self.save_btn_on_click)
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

        # Refresh and display the dashboard values
        self.refresh_dashboard()


    def show_error(self, message):
        '''Display error message when invalid input'''
        messagebox.showerror("Error", message)
    
        
    def refresh_dashboard(self):
        '''refresh money details, transaction table, member balance, and settlement'''
        # get trip data from json file
        expenses_list = self.trip_info_dict.get("expenses", [])
        currency = self.trip_info_dict.get("base_currency", "NZD")
        group_members = self.trip_info_dict.get("members", [])

        total_sum = 0.0
        for item in expenses_list:
            total_sum= total_sum + item.get("amount", 0.0)

        self.lbl_total_cost.configure(text=f"Total Cost: ${total_sum:.2f} ({currency})")

        for child in self.transactions_scrollable_frame.winfo_children():
            child.destroy()

        for item in expenses_list:
            row_frame = ctk.CTkFrame(self.transactions_scrollable_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            lbl_date = ctk.CTkLabel(row_frame, text=item.get("date", "N/A"), width=85, anchor="w")
            lbl_date.pack(side="left", padx=(5, 5))

            lbl_description = ctk.CTkLabel(row_frame, text=item.get("description", "No description"), width=160, anchor="w")
            lbl_description.pack(side="left", padx=5)

            lbl_category = ctk.CTkLabel(row_frame, text=item.get("category", "other"), width=110, anchor="w")
            lbl_category.pack(side="left", padx=5)

            lbl_payer = ctk.CTkLabel(row_frame, text=item.get("payer", "other"), width=75, anchor="w")
            lbl_payer.pack(side="left", padx=5)

            lbl_amount = ctk.CTkLabel(row_frame, text=item.get("amount", 0.0), width=75, anchor="w")
            lbl_amount.pack(side="left",  padx=5)

            # Actions frame holding edit and delete buttons (fixed 60px width)
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=60)
            action_frame.pack(side="left", padx=5)

            btn_edit = ctk.CTkButton(action_frame, text="", image=self.edit_icon, width=24, height=24, fg_color="transparent", hover_color="#E0E0E0", command=lambda x=item: self.edit_expense_btn_on_click(x))
            btn_edit.pack(side="left", padx=1)

            btn_delete = ctk.CTkButton(action_frame, text="", image=self.delete_icon, width=24, height=24, fg_color="transparent", hover_color="#FFE5E5", command=lambda x=item: self.delete_expense(x))
            btn_delete.pack(side="left", padx=1)

        # using winfo.children to clear all widgets from the member box.
        for child in self.member_scrollable_box.winfo_children():
            child.destroy()

        self.btn_manage_member = ctk.CTkButton(self.member_scrollable_box, text="Add/Remove member", height=30, command=self.manage_member_btn_on_click)
        self.btn_manage_member.pack(padx=10, pady=(0, 10))
        
        member_balances = {}
        for member_name in group_members:
            member_balances[member_name] = 0.0

        for item in expenses_list:
            payer_name = item.get("payer", "")
            amount_paid = item.get("amount", 0.0)
            split_list = item.get("split_between", group_members)

            if payer_name in member_balances:
                member_balances[payer_name] = member_balances[payer_name] + amount_paid

            if len(split_list) > 0:
                share_amount = amount_paid / len(split_list)
                for person in split_list:
                    if person in member_balances:
                        member_balances[person] = member_balances[person] - share_amount

        for member_name in group_members:
            net_balance = member_balances.get(member_name, 0.0)
            if net_balance >= 0:
                status_text = f"{member_name}: +${net_balance:.2f} (Debit)"
                text_color_val = "#00A86B"
            else:
                positive_amount = net_balance * -1
                status_text = f"{member_name}: -${positive_amount:.2f} (Credit)"
                text_color_val = "#FF4D4D"

            lbl_member_balance = ctk.CTkLabel(self.member_scrollable_box, text=status_text, text_color=text_color_val, font=ctk.CTkFont(size=12, weight="bold"))
            lbl_member_balance.pack(anchor="w", padx=5, pady=3)

        # settlement calculation
        for child in self.settlements_scroll_box.winfo_children():
            child.destroy()

        for member_name in group_members:
            if member_balances[member_name] < -0.01:
                for creditor in group_members:
                    if member_balances[creditor] > 0.01:
                        settlement_text = f"{member_name} owes {creditor}"
                        lbl_settlement = ctk.CTkLabel(self.settlements_scroll_box, text=settlement_text, font=ctk.CTkFont(size=12))
                        lbl_settlement.pack(anchor="w", pady=2)
                        break

        # Calculate overall per-person split estimate
        if len(group_members) > 0:
            per_person_split = total_sum / len(group_members)
        else:
            per_person_split = 0.0
        
        
    def delete_expense(self, item):
        '''Removes an expense item from the list'''
        if item in self.trip_info_dict.get("expenses", []):
            self.trip_info_dict["expenses"].remove(item)
            self.save_trip_data()
            self.refresh_dashboard()


    def edit_expense_btn_on_click(self, item=None):
        '''Action when edit expense button is clicked'''
        # Placeholder for editing an expense
        print("Edit expense button clicked")


    def add_expense_btn_on_click(self):
        '''Action when add expense button is clicked'''
        # Placeholder for adding an expense
        print("Add expense button clicked")
        
    
    def save_trip_data(self):
        '''Saves current trip dictionary state back into the JSON file'''
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.trip_info_dict, f, indent=4)
        except FileNotFoundError:
            self.show_error("Could not find the trip file to save changes!")


    def save_btn_on_click(self):
        '''Save the trip data into a json file'''
        self.save_trip_data()
        messagebox.showinfo("Success", "Trip Data has been saved successfully")


    def manage_member_btn_on_click(self):
        '''Action when add/remove member button is clicked'''
        # placeholder for managing members
        print("Manage member button clicked")


    def back_btn_on_click(self):
        '''Return to the launcher window'''
        # placeholder for returning to launcher window
        print("back to main menu")
        


root = ctk.CTk()
app = TripDashboard(root)
root.mainloop()
