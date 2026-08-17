
# Purpose: This window allow users to enter expense details (title, amount, date, payer, description, and member spliting boxes ) to a trip json file.
# Author: Hubert Kwan
# Date: 10/08/2026
# Version: 1.1 

# This version has implement a callback funtion which controlled by the main program.
# It also has fixed bugs and errors during testing.
# It also uncommented the toplevel window and change self.root to self.top. To transform it to a pop-up window so it will not crash with trip dashboard.


# import libraries and modules
import os 
import json
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

# Set up app appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ExpenseFormWindow:
    def __init__(self, root, file_path="trip/japan.json", on_save_callback=None):
        '''initialse the form window, with loading trip data and the UI'''
        self.root = root
        self.top = ctk.CTkToplevel(root)
        self.top.title("Expense Management Window")
        self.top.geometry("400x650")
        self.top.lift()
        
        self.file_path = file_path
        self.on_save_callback = on_save_callback
        self.trip_info_dict = {}
        self.members_list = []
        # dictory to store expense split variables
        self.checkbox_widget = {}
        
        if os.path.exists(self.file_path):
            self.load_trip_file()
        else:
            self.members_list = ["Alice", "Bob", "Charlie"]

        # Configure pop-up window grid columns
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)

        # Build all form input fields
        self.create_widgets()
        
    
    def load_trip_file(self):
        '''Loads member list safely from json file'''
        try:
            with open(self.file_path, "r", encoding="utf-8") as file_data:
                self.trip_info_dict = json.load(file_data)
                self.members_list = self.trip_info_dict("members", [])
        except FileNotFoundError:
            self.show_error("Could not find the trip file to load members")
            
    
    def create_widgets(self):
        '''Create all input fields, labels, option menus, and buttons '''
        # Heading label
        self.lbl_window_title = ctk.CTkLabel(self.top, text="Add/Edit Expense", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_window_title.grid(row=0, column=0, columnspan=2, pady=(15, 10))
        # Expense title label
        self.lbl_expense_title = ctk.CTkLabel(self.top, text="Title", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_expense_title.grid(row=1, column=0, columnspan=2, padx=20, pady=(5, 2), sticky="w")
        # Expense title entry box
        self.entry_expense_title = ctk.CTkEntry(self.top, placeholder_text="e.g. Dinner in Sushiro", justify="center")
        self.entry_expense_title.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="ew")
        # Amount label
        self.lbl_amount = ctk.CTkLabel(self.top, text="Amount", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_amount.grid(row=3, column=0, columnspan=2, padx=20, pady=(5, 2), sticky="w")
        # Amount entry box
        self.entry_amount = ctk.CTkEntry(self.top, placeholder_text="e.g. $50", justify="center")
        self.entry_amount.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="ew")
        
        self.lbl_date = ctk.CTkLabel(self.top, text="Date", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_date.grid(row=5, column=0, padx=(20, 5), pady=(5,2), sticky="w")

        self.entry_date = ctk.CTkEntry(self.top, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_date.grid(row=6, column=0, padx=(20, 5), pady=(0, 8), sticky="ew")
        
        self.lbl_category = ctk.CTkLabel(self.top, text="Category", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_category.grid(row=5, column=1, padx=(5, 20), pady=(5, 2), sticky="w")
        self.combo_category = ctk.CTkOptionMenu(self.top, values=["Food", "Transport", "Accommodation", "Activities", "Other"])
        self.combo_category.grid(row=6, column=1, padx=(5, 20), pady=(0, 8), sticky="ew")
        
        self.lbl_payer = ctk.CTkLabel(self.top, text="Payer", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_payer.grid(row=7, column=0, columnspan=2, padx=20, pady=(5, 2), sticky="w")
        
        if len(self.members_list) > 0:
            payer_options = self.members_list
        else:
            payer_options = ["No member was found."]
        self.combo_payer = ctk.CTkOptionMenu(self.top, values=payer_options)
        self.combo_payer.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
        
        self.lbl_assign = ctk.CTkLabel(self.top, text="Assign Shares(Equal split)", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_assign.grid(row=9, column=0, columnspan=2, padx=20, pady=(5, 2), sticky="w")
        
        self.member_scrcoll_box = ctk.CTkScrollableFrame(self.top, height=130)
        self.member_scrcoll_box.grid(row=10, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="nsew")
        
        if len(self.members_list) == 0:
            lbl_no_member = ctk.CTkLabel(self.member_scrcoll_box, text="No member in trip file", text_color="grey")
            lbl_no_member.pack(pady=10)
        else:
            for person_name in self.members_list:
                row_frame = ctk.CTkFrame(self.member_scrcoll_box, fg_color="transparent")
                row_frame.pack(fill="x", pady=3)
                
                chk_var = ctk.BooleanVar(value=True)
                chk_box = ctk.CTkCheckBox(row_frame, text=person_name, variable=chk_var)
                chk_box.pack(side="left", padx=5)
                
                self.checkbox_widget[person_name] = chk_var
                
            
        self.btn_cancel = ctk.CTkButton(self.top, text="Cancel", fg_color="gray", hover_color="#555555", command=self.top.destroy)
        self.btn_cancel.grid(row=11, column=0, padx=(20, 5), pady=(0, 15), sticky='ew')
        self.btn_confirm = ctk.CTkButton(self.top, text="Confirm", fg_color="#0080ff", command=self.confirm_btn_on_click)
        self.btn_confirm.grid(row=11, column=1, padx=(5, 20), pady=(0, 15), sticky="ew")
            

    def show_error(self, message):
        '''methods to show error message'''
        messagebox.showerror("Error", message, parent=self.top)
        
    
    def validate_inputs(self):
        '''validates form inputs before create=ing the expense dictionary'''
        title = self.entry_expense_title.get().strip()
        amount = self.entry_amount.get().strip()
        date = self.entry_date.get().strip()
        
        if title == "":
            self.show_error("Expense title cannot be blank!")
            return False
        try:
            clean_amount = amount.replace("$", "")
            parsed_amount = float(clean_amount)
            if parsed_amount <= 0:
                self.show_error("Amount must be a positive number!")
                return False
        except ValueError:
            self.show_error("Please enter a valid number for 'Amount'.")
            return False
        
        if date == "":
            self.show_error("Date cannot be blank!")
            return False
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            self.show_error("Date must be in the format of dd/mm/yyyy.")
            return False
        return True
    
    
    def confirm_btn_on_click(self):
        '''process input data and append the nre epxense dictionary to the json file'''
        if not self.validate_inputs():
            return
        
        title = self.entry_expense_title.get().strip()
        amount_value = float(self.entry_amount.get().replace("$", "").strip())
        date_value = self.entry_date.get().strip()
        category = self.combo_category.get()
        payer = self.combo_payer.get()
        
        selected_members = []
        for person_name, chk_var in self.checkbox_widget.items():
            if chk_var.get() == True:
                selected_members.append(person_name)
                
        if len(selected_members) == 0:
            self.show_error("Please select at least one member to split the expense!")
            return
        
        split_share_amount = amount_value / len(selected_members)
        
        expense_dict = {
            "title": title,
            "description": title,
            "amount": amount_value,
            "date": date_value,
            "category": category,
            "payer": payer,
            "split_between": selected_members,
            "share_per_person": round(split_share_amount, 2)
        }

        if os.path.exists(self.file_path):
            try:
                if "expenses" not in self.trip_info_dict:
                    self.trip_info_dict["expenses"] = []
                self.trip_info_dict["expenses"].append(expense_dict)

                with open(self.file_path, "w", encoding="utf-8") as file_data:
                    json.dump(self.trip_info_dict, file_data, indent=4)
            except FileNotFoundError:
                self.show_error("Could not find the trip file to write changes!")
                return
            
        if self.on_save_callback:
            self.on_save_callback(expense_dict)

        messagebox.showinfo("Success", f"Expense '{title}' successfully added to trip!", parent=self.top)
        self.top.destroy()


# run the current window
# comment out the window runner which only display the window when called in main program.
# root = ctk.CTk()
# app = ExpenseFormWindow(root)
# root.mainloop()
