# Purpose: Component 3 is to display detail of chosen trip, transactions search filter, refined settlement, and member balance.
# Author: Hubert Kwan
# Date: 20/08/2026
# Version: 2.1

# Improvements:
# 1. Added a transaction detail window. This window will only be visible when a user click on an expense title with a underline style. It then pop-up the transaction to view the detail like split breakdown. The window also provide a button to change to edit mode to make changes for the transaction.

# Import required libraries and modules
import os
import json
import customtkinter as ctk
from PIL import Image
from datetime import datetime
from tkinter import messagebox

# Constants
DEFAULT_CURRENCY = "NZD"
EXPENSE_CATEGORIES = ["All Categories", "Food", "Transport", "Accommodation", "Activities", "Other"]

# UI Theme Color Constants
COLOR_ADD_EXPENSE_BTN = "#0080FF"
COLOR_SAVE_BTN = "#00A86B"
COLOR_CLEAR_BTN = "gray"
COLOR_BACK_BTN = "gray"
COLOR_BACK_HOVER_BTN = "#555555"
COLOR_DEBIT_TEXT = "#00A86B"
COLOR_CREDIT_TEXT = "#FF4D4D"
COLOR_TABLE_HEADER_BG = "#adadad"
COLOR_EDIT_HOVER_BG = "#E0E0E0"
COLOR_DELETE_HOVER_BG = "#FFE5E5"

# Set default appearance mode and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class TripDashboard:
    '''Main GUI window class for displaying trip summary and expense details'''
    def __init__(self, root, file_path=None):
        '''Initialises the dashboard window and loads trip data'''
        self.root = root
        self.root.title("Trip Dashboard")
        self.root.geometry("1200x550")
        
        self.file_path = file_path
        self.trip_info_dict = {}

        # Callback function placeholders for main controller connection
        self.add_expense_btn_on_click_callback = None
        self.edit_expense_btn_on_click_callback = None
        self.manage_member_btn_on_click_callback = None
        self.edit_trip_details_callback = None
        self.back_btn_on_click_callback = None
        self.view_expense_detail_callback = None

        # Load icon images for delete and edit action buttons with safety fallback
        try:
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
        except FileNotFoundError:
            self.delete_icon = None
            self.edit_icon = None
        
        # Grid layout row/column configurations for responsive layout resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Load JSON file if path is valid
        if self.file_path != None and os.path.exists(self.file_path) == True:
            self.load_trip_file()
        
        # Build dashboard GUI layout
        self.create_widgets()
        
    def load_trip_file(self):
        '''Loads trip details safely from the selected JSON file'''
        if self.file_path == None:
            return

        try:
            # Read JSON file content into trip_info_dict
            with open(self.file_path, "r", encoding="utf-8") as file_data:
                self.trip_info_dict = json.load(file_data)
        except FileNotFoundError:
            self.show_error(f"Could not find trip file '{self.file_path}'!")

    def create_widgets(self):
        '''creates trip dashboard layout'''
        # Top banner title frame containing trip name, pencil edit button, theme switch, and back button
        self.top_title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_title_frame.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        
        trip_name = self.trip_info_dict.get("name", "Trip Dashboard")
        self.lbl_trip_title = ctk.CTkLabel(self.top_title_frame, text=f"Trip: {trip_name}", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_trip_title.pack(side="left")

        # Edit trip details pencil icon button
        if self.edit_icon != None:
            self.btn_edit_trip_details = ctk.CTkButton(self.top_title_frame, text="", image=self.edit_icon, width=28, height=28, fg_color="transparent", hover_color=COLOR_EDIT_HOVER_BG, command=self.edit_trip_click)
        else:
            self.btn_edit_trip_details = ctk.CTkButton(self.top_title_frame, text="✏", width=28, height=28, fg_color="transparent", hover_color=COLOR_EDIT_HOVER_BG, command=self.edit_trip_click)
        self.btn_edit_trip_details.pack(side="left", padx=8)

        # Global theme toggle switch
        self.theme_switch = ctk.CTkSwitch(self.top_title_frame, text="Light/Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="right", padx=10)
        
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

        # Back button returning to launcher
        self.btn_back = ctk.CTkButton(self.top_title_frame, text="Back", width=80, fg_color=COLOR_BACK_BTN, hover_color=COLOR_BACK_HOVER_BTN, command=self.back_btn_on_click)
        self.btn_back.pack(side="right")
        
        # Main body split frame divided into left/right sections
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Left side column container
        self.middle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.middle_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(2, weight=1)
        
        # Total trip cost banner display
        self.total_cost_box = ctk.CTkFrame(self.middle_frame, height=45, corner_radius=8)
        self.total_cost_box.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        
        self.lbl_total_cost = ctk.CTkLabel(self.total_cost_box, text="Total Cost: $0.00", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_total_cost.pack(side="left", padx=15, pady=8)
        
        # Search & Category Filter bar aligned to the right
        self.search_filter_frame = ctk.CTkFrame(self.middle_frame, fg_color="transparent")
        self.search_filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        # Clear filter button
        self.btn_clear_filter = ctk.CTkButton(self.search_filter_frame, text="Clear", width=60, fg_color=COLOR_CLEAR_BTN, command=self.clear_filter_click)
        self.btn_clear_filter.pack(side="right", padx=(5, 0))

        # Category dropdown filter option menu
        self.option_filter_category = ctk.CTkOptionMenu(
            self.search_filter_frame, 
            values=EXPENSE_CATEGORIES,
            command=lambda v: self.refresh_dashboard()
        )
        self.option_filter_category.pack(side="right", padx=5)

        # Keyword search entry field
        self.entry_search_keyword = ctk.CTkEntry(self.search_filter_frame, placeholder_text="Search title or date...", width=160)
        self.entry_search_keyword.pack(side="right", padx=5)
        self.entry_search_keyword.bind("<KeyRelease>", lambda e: self.refresh_dashboard())

        # Lower split container for member balances and transactions table
        self.lower_split_frame = ctk.CTkFrame(self.middle_frame, fg_color="transparent")
        self.lower_split_frame.grid(row=2, column=0, sticky="nsew")
        self.lower_split_frame.grid_columnconfigure(0, weight=1)
        self.lower_split_frame.grid_columnconfigure(1, weight=3)
        self.lower_split_frame.grid_rowconfigure(0, weight=1)
        
        # Member individual balance box section
        self.member_balance_box = ctk.CTkFrame(self.lower_split_frame, corner_radius=10)
        self.member_balance_box.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        self.lbl_balance_title = ctk.CTkLabel(self.member_balance_box, text="Member Balances", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_balance_title.pack(pady=10)
        
        self.member_scrollable_box = ctk.CTkScrollableFrame(self.member_balance_box, fg_color="transparent")
        self.member_scrollable_box.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Main transactions table container and fixed table headers
        self.table_container_frame = ctk.CTkFrame(self.lower_split_frame, fg_color="transparent")
        self.table_container_frame.grid(row=0, column=1, sticky="nsew")
        self.table_container_frame.grid_columnconfigure(0, weight=1)
        self.table_container_frame.grid_rowconfigure(1, weight=1)
        
        self.table_header_frame = ctk.CTkFrame(self.table_container_frame, height=35, fg_color=COLOR_TABLE_HEADER_BG)
        self.table_header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
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
        
        # Scrollable area rendering individual transaction rows dynamically
        self.transactions_scrollable_frame = ctk.CTkScrollableFrame(self.table_container_frame)
        self.transactions_scrollable_frame.grid(row=1, column=0, sticky="nsew")
        
        # Right column containing main actions and settlement algorithm breakdown
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Add new expense button
        self.btn_add_expense = ctk.CTkButton(self.right_frame, text="+ Add Expense", fg_color=COLOR_ADD_EXPENSE_BTN, height=35, command=self.add_expense_btn_on_click)
        self.btn_add_expense.pack(fill="x", pady=(0, 8))
        
        # Save changes button
        self.btn_save_changes = ctk.CTkButton(self.right_frame, text="✔ Save Changes", fg_color=COLOR_SAVE_BTN, height=35, command=self.save_btn_on_click)
        self.btn_save_changes.pack(fill="x", pady=(0, 15))
        
        # Settlement breakdown card section
        self.settlement_box = ctk.CTkFrame(self.right_frame, corner_radius=10)
        self.settlement_box.pack(fill="both", expand=True)

        self.lbl_settle_title = ctk.CTkLabel(self.settlement_box, text="Settlement Breakdown", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_settle_title.pack(pady=10)

        self.settlements_scroll_box = ctk.CTkScrollableFrame(self.settlement_box, fg_color="transparent")
        self.settlements_scroll_box.pack(fill="both", expand=True, padx=5, pady=5)

        # Trigger full refresh calculation and render on view load
        self.refresh_dashboard()

    def edit_trip_click(self):
        # Trigger edit trip callback to controller
        if self.edit_trip_details_callback:
            self.edit_trip_details_callback()

    def clear_filter_click(self):
        # Reset search bar and dropdown filter controls
        self.entry_search_keyword.delete(0, "end")
        self.option_filter_category.set(EXPENSE_CATEGORIES[0])
        self.refresh_dashboard()

    def toggle_theme(self):
        '''Toggles Light/Dark mode globally'''
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def show_error(self, message):
        '''Display error message when invalid input'''
        messagebox.showerror("Error", message, parent=self.root)

    def view_expense_detail_click(self, item):
        '''Callback trigger to open Component 5 detail window pop-up'''
        if self.view_expense_detail_callback:
            self.view_expense_detail_callback(item)

    def refresh_dashboard(self):
        '''refresh money details, filtered transaction table, member balance, and settlement'''
        # Extract data lists safely from dictionary
        expenses_list = self.trip_info_dict.get("expenses", [])
        currency = self.trip_info_dict.get("base_currency", DEFAULT_CURRENCY)
        group_members = self.trip_info_dict.get("members", [])

        # Calculate total cost sum across all expenses
        total_sum = 0.0
        for item in expenses_list:
            total_sum = total_sum + item.get("amount", 0.0)

        self.lbl_total_cost.configure(text=f"Total Cost: ${total_sum:.2f} ({currency})")

        # Clear existing rows in transactions scrollable frame
        for child in self.transactions_scrollable_frame.winfo_children():
            child.destroy()

        # Get search filter inputs
        search_kw = self.entry_search_keyword.get().strip().lower()
        filter_cat = self.option_filter_category.get()

        # Filter expenses list according to search keywords and selected category
        for item in expenses_list:
            item_title = item.get("title", item.get("description", "")).lower()
            item_date = item.get("date", "").lower()
            item_category = item.get("category", "Other")

            # Match search terms against expense title or date string
            keyword_match = False
            if search_kw == "":
                keyword_match = True
            elif search_kw in item_title:
                keyword_match = True
            elif search_kw in item_date:
                keyword_match = True

            # Match category selection
            category_match = False
            if filter_cat == EXPENSE_CATEGORIES[0]:
                category_match = True
            elif filter_cat == item_category:
                category_match = True

            # Render row if both filter criteria match
            if keyword_match == True and category_match == True:
                row_frame = ctk.CTkFrame(self.transactions_scrollable_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=2)

                lbl_date = ctk.CTkLabel(row_frame, text=item.get("date", "N/A"), width=85, anchor="w")
                lbl_date.pack(side="left", padx=(5, 5))

                # Clickable underlined description label triggering component 5 pop-up view
                lbl_description = ctk.CTkLabel(
                    row_frame, 
                    text=item.get("title", item.get("description", "No description")), 
                    width=160, 
                    anchor="w", 
                    font=ctk.CTkFont(size=13, underline=True),
                    text_color=("black", "white"),
                    cursor="hand2"
                )
                lbl_description.pack(side="left", padx=5)
                lbl_description.bind("<Button-1>", lambda event, exp=item: self.view_expense_detail_click(exp))

                lbl_category = ctk.CTkLabel(row_frame, text=item.get("category", "other"), width=110, anchor="w")
                lbl_category.pack(side="left", padx=5)

                lbl_payer = ctk.CTkLabel(row_frame, text=item.get("payer", "other"), width=75, anchor="w")
                lbl_payer.pack(side="left", padx=5)

                lbl_amount = ctk.CTkLabel(row_frame, text=f"${item.get('amount', 0.0):.2f}", width=75, anchor="w")
                lbl_amount.pack(side="left", padx=5)

                # Action button container for edit and delete triggers per row
                action_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=60)
                action_frame.pack(side="left", padx=5)

                if self.edit_icon != None:
                    btn_edit = ctk.CTkButton(action_frame, text="", image=self.edit_icon, width=24, height=24, fg_color="transparent", hover_color=COLOR_EDIT_HOVER_BG, command=lambda exp=item: self.edit_expense_btn_on_click(exp))
                else:
                    btn_edit = ctk.CTkButton(action_frame, text="Edit", width=24, height=24, fg_color="transparent", hover_color=COLOR_EDIT_HOVER_BG, command=lambda exp=item: self.edit_expense_btn_on_click(exp))
                btn_edit.pack(side="left", padx=1)

                if self.delete_icon != None:
                    btn_delete = ctk.CTkButton(action_frame, text="", image=self.delete_icon, width=24, height=24, fg_color="transparent", hover_color=COLOR_DELETE_HOVER_BG, command=lambda exp=item: self.delete_expense(exp))
                else:
                    btn_delete = ctk.CTkButton(action_frame, text="X", width=24, height=24, fg_color="transparent", hover_color=COLOR_DELETE_HOVER_BG, command=lambda exp=item: self.delete_expense(exp))
                btn_delete.pack(side="left", padx=1)

        # Clear existing member balance widget displays
        for child in self.member_scrollable_box.winfo_children():
            child.destroy()

        # Add/Remove member button placed inside member section
        self.btn_manage_member = ctk.CTkButton(self.member_scrollable_box, text="Add/Remove member", height=30, command=self.manage_member_btn_on_click)
        self.btn_manage_member.pack(padx=10, pady=(0, 10))

        # Initialize balances dictionary for each member
        member_balances = {}
        for member_name in group_members:
            member_balances[member_name] = 0.0

        # Calculate individual member balances considering payer additions and share deductions
        for item in expenses_list:
            payer_name = item.get("payer", "")
            amount_paid = item.get("amount", 0.0)
            split_list = item.get("split_between", group_members)
            custom_dict = item.get("custom_shares", {})

            # Credit payer full amount
            if payer_name in member_balances:
                member_balances[payer_name] = member_balances[payer_name] + amount_paid

            # Debit split shares (either custom amounts or equal split shares)
            if len(custom_dict) > 0:
                for person_name, share_val in custom_dict.items():
                    if person_name in member_balances:
                        member_balances[person_name] = member_balances[person_name] - share_val
            else:
                if len(split_list) > 0:
                    share_amount = amount_paid / len(split_list)
                    for person in split_list:
                        if person in member_balances:
                            member_balances[person] = member_balances[person] - share_amount

        # Display member balance status labels with green/red color 
        for member_name in group_members:
            net_balance = member_balances.get(member_name, 0.0)
            if net_balance >= 0:
                status_text = f"{member_name}: +${net_balance:.2f} (Debit)"
                text_color_val = COLOR_DEBIT_TEXT
            else:
                positive_amount = net_balance * -1
                status_text = f"{member_name}: -${positive_amount:.2f} (Credit)"
                text_color_val = COLOR_CREDIT_TEXT

            lbl_member_balance = ctk.CTkLabel(self.member_scrollable_box, text=status_text, text_color=text_color_val, font=ctk.CTkFont(size=12, weight="bold"))
            lbl_member_balance.pack(anchor="w", padx=5, pady=3)

        # Clear existing settlement widgets
        for child in self.settlements_scroll_box.winfo_children():
            child.destroy()

        # Classify members into debtors and creditors
        debtors = []
        creditors = []
        for name, bal in member_balances.items():
            if bal < -0.01:
                debtors.append([name, abs(bal)])
            elif bal > 0.01:
                creditors.append([name, bal])

        # Run settlement calculation algorithm to minimize transfer counts
        for debtor in debtors:
            d_name = debtor[0]
            d_amount = debtor[1]
            for creditor in creditors:
                c_name = creditor[0]
                c_amount = creditor[1]

                if d_amount > 0 and c_amount > 0:
                    if d_amount < c_amount:
                        settle_val = d_amount
                    else:
                        settle_val = c_amount

                    d_amount = d_amount - settle_val
                    creditor[1] = creditor[1] - settle_val

                    # Render settlement text statement line
                    settlement_text = f"{d_name} owes {c_name} ${settle_val:.2f}"
                    lbl_settlement = ctk.CTkLabel(self.settlements_scroll_box, text=settlement_text, font=ctk.CTkFont(size=12))
                    lbl_settlement.pack(anchor="w", pady=2)

    def delete_expense(self, item):
        '''Removes an expense item from the list'''
        if item in self.trip_info_dict.get("expenses", []):
            self.trip_info_dict["expenses"].remove(item)
            self.save_trip_data()
            self.refresh_dashboard()

    def edit_expense_btn_on_click(self, item=None):
        '''Action when edit expense button is clicked'''
        if self.edit_expense_btn_on_click_callback:
            self.edit_expense_btn_on_click_callback(item)

    def add_expense_btn_on_click(self):
        '''Action when add expense button is clicked'''
        if self.add_expense_btn_on_click_callback:
            self.add_expense_btn_on_click_callback()

    def save_trip_data(self):
        '''Saves current trip dictionary state back into the JSON file'''
        if self.file_path == None:
            self.show_error("No file path set to save trip data!")
            return

        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.trip_info_dict, f, indent=4)
        except FileNotFoundError:
            self.show_error("Could not find the trip file to save changes!")

    def save_btn_on_click(self):
        '''Save the trip data into a json file'''
        self.save_trip_data()
        messagebox.showinfo("Success", "Trip Data has been saved successfully", parent=self.root)

    def manage_member_btn_on_click(self):
        '''Action when add/remove member button is clicked'''
        if self.manage_member_btn_on_click_callback:
            self.manage_member_btn_on_click_callback()

    def back_btn_on_click(self):
        '''Return to the launcher window'''
        if self.back_btn_on_click_callback:
            self.back_btn_on_click_callback()
