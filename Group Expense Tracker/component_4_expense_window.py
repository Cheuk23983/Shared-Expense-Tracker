
# Purpose: This window allow users to enter expense details (title, amount, date, payer, description, and member spliting boxes ) to a trip json file.
# Author: Hubert Kwan
# Date: 18/08/2026
# Version: 1.2

# This version include fixed bugs and error when intergrate with the main program



# import libraries and modules
import os 
import json
from datetime import datetime
import customtkinter as ctk
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


class ExpenseFormWindow:
    def __init__(self, root, file_path=None, on_save_callback=None, on_cancel_callback=None, edit_item=None):
        '''initialse the form window, with loading trip data and the UI'''
        self.root = root
        self.file_path = file_path
        self.on_save_callback = on_save_callback
        self.on_cancel_callback = on_cancel_callback
        self.edit_item = edit_item
        
        self.trip_info_dict = {}
        self.members_list = []
        self.checkbox_widget = {}
        self.custom_entry_widget = {}
        self.manual_split_mode = False
        
        if self.file_path != None and os.path.exists(self.file_path) == True:
            self.load_trip_file()
        
        if len(self.members_list) == 0:
            self.members_list = ["Alice", "Bob", "Charlie"]

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def load_trip_file(self):
        '''Loads member list safely from json file'''
        if self.file_path == None:
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file_data:
                self.trip_info_dict = json.load(file_data)
                self.members_list = self.trip_info_dict.get("members", [])
        except FileNotFoundError:
            self.show_error("Could not find the trip file to load members.")

    def create_widgets(self):
        '''Create all input fields, labels, option menus, and buttons '''
        if self.edit_item != None:
            title_heading = "Edit Expense"
        else:
            title_heading = "Add Expense"
            
        self.lbl_window_title = ctk.CTkLabel(self.root, text=title_heading, font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_window_title.grid(row=0, column=0, columnspan=2, pady=(15, 10))

        # Expense title
        self.lbl_expense_title = ctk.CTkLabel(self.root, text="Title", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_expense_title.grid(row=1, column=0, columnspan=2, padx=20, pady=(5, 2), sticky="w")
        self.entry_expense_title = ctk.CTkEntry(self.root, placeholder_text="e.g. Dinner in Sushiro", justify="center")
        self.entry_expense_title.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="ew")

        # Amount
        self.lbl_amount = ctk.CTkLabel(self.root, text="Amount", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_amount.grid(row=3, column=0, columnspan=2, padx=20, pady=(5, 2), sticky="w")
        self.entry_amount = ctk.CTkEntry(self.root, placeholder_text="e.g. $50", justify="center")
        self.entry_amount.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="ew")
        
        self.lbl_date = ctk.CTkLabel(self.root, text="Date (Within Trip Period)", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_date.grid(row=5, column=0, padx=(20, 5), pady=(5, 2), sticky="w")
        
        self.date_input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.date_input_frame.grid(row=6, column=0, padx=(20, 5), pady=(0, 8), sticky="ew")
        
        self.entry_date = ctk.CTkEntry(self.date_input_frame, placeholder_text="dd/mm/yyyy", justify="center")
        self.entry_date.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_pick_date = ctk.CTkButton(self.date_input_frame, text="📅", width=35, command=lambda: self.open_date_picker(self.entry_date))
        self.btn_pick_date.pack(side="right")
        
        # Category
        self.lbl_category = ctk.CTkLabel(self.root, text="Category", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_category.grid(row=5, column=1, padx=(5, 20), pady=(5, 2), sticky="w")
        self.combo_category = ctk.CTkOptionMenu(self.root, values=["Food", "Transport", "Accommodation", "Activities", "Other"])
        self.combo_category.grid(row=6, column=1, padx=(5, 20), pady=(0, 8), sticky="ew")
        
        # Payer
        self.lbl_payer = ctk.CTkLabel(self.root, text="Payer", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_payer.grid(row=7, column=0, columnspan=2, padx=20, pady=(5, 2), sticky="w")
        
        if len(self.members_list) > 0:
            payer_options = self.members_list
        else:
            payer_options = ["No member found."]
            
        self.combo_payer = ctk.CTkOptionMenu(self.root, values=payer_options)
        self.combo_payer.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 6), sticky="ew")
        
        self.split_switch = ctk.CTkSwitch(self.root, text="Manual Split Mode ($)", command=self.toggle_split_mode)
        self.split_switch.grid(row=9, column=0, columnspan=2, padx=20, pady=4, sticky="w")

        # Assign shares scroll box
        self.member_scrcoll_box = ctk.CTkScrollableFrame(self.root, height=120)
        self.member_scrcoll_box.grid(row=10, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="nsew")
        
        self.render_member_split_list()

        # Theme Switch
        self.theme_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.theme_frame.grid(row=11, column=0, columnspan=2, padx=20, pady=2)
        self.theme_switch = ctk.CTkSwitch(self.theme_frame, text="Light/Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack()
        
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

        # Action Buttons
        self.btn_cancel = ctk.CTkButton(self.root, text="Cancel", fg_color="gray", hover_color="#555555", command=self.cancel_btn_click)
        self.btn_cancel.grid(row=12, column=0, padx=(20, 5), pady=(5, 15), sticky='ew')
        
        self.btn_confirm = ctk.CTkButton(self.root, text="Confirm", fg_color="#0080ff", command=self.confirm_btn_on_click)
        self.btn_confirm.grid(row=12, column=1, padx=(5, 20), pady=(5, 15), sticky="ew")

        if self.edit_item != None:
            self.entry_expense_title.insert(0, self.edit_item.get("title", ""))
            self.entry_amount.insert(0, str(self.edit_item.get("amount", "")))
            self.entry_date.insert(0, self.edit_item.get("date", ""))
            self.combo_category.set(self.edit_item.get("category", "Food"))
            self.combo_payer.set(self.edit_item.get("payer", self.members_list[0]))

    def open_date_picker(self, target_entry):
        '''DatePicker popup window'''
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

    def toggle_split_mode(self):
        '''Toggle between Equal Split and Manual Split Mode'''
        if self.split_switch.get() == 1:
            self.manual_split_mode = True
        else:
            self.manual_split_mode = False
        self.render_member_split_list()

    def render_member_split_list(self):
        ''' cahnge between equal checkboxes or right-aligned manual split entry boxes'''
        for child in self.member_scrcoll_box.winfo_children():
            child.destroy()

        self.checkbox_widget = {}
        self.custom_entry_widget = {}

        if self.edit_item != None:
            split_preselect = self.edit_item.get("split_between", self.members_list)
            custom_shares = self.edit_item.get("custom_shares", {})
        else:
            split_preselect = self.members_list
            custom_shares = {}

        for person_name in self.members_list:
            row_frame = ctk.CTkFrame(self.member_scrcoll_box, fg_color="transparent")
            row_frame.pack(fill="x", pady=3)

            if self.manual_split_mode == False:
                # Equal split checkbox mode
                if person_name in split_preselect:
                    chk_var = ctk.BooleanVar(value=True)
                else:
                    chk_var = ctk.BooleanVar(value=False)
                    
                chk_box = ctk.CTkCheckBox(row_frame, text=person_name, variable=chk_var)
                chk_box.pack(side="left", padx=5)
                self.checkbox_widget[person_name] = chk_var
            else:
                # Manual split entry box mode aligned right
                lbl = ctk.CTkLabel(row_frame, text=person_name, width=100, anchor="w")
                lbl.pack(side="left", padx=5)

                amt_entry = ctk.CTkEntry(row_frame, placeholder_text="0.00", width=80, justify="center")
                amt_entry.pack(side="right", padx=5)

                if person_name in custom_shares:
                    amt_entry.insert(0, str(custom_shares[person_name]))
                self.custom_entry_widget[person_name] = amt_entry

    def toggle_theme(self):
        '''Toggles Light/Dark mode globally'''
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def show_error(self, message):
        '''methods to show error message'''
        messagebox.showerror("Error", message, parent=self.root)

    def cancel_btn_click(self):
        '''Return to dashboard view'''
        if self.on_cancel_callback:
            self.on_cancel_callback()
        
    def validate_inputs(self):
        '''validates form inputs before creating/updating expense'''
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
            expense_dt = datetime.strptime(date, "%d/%m/%Y")
            trip_start_str = self.trip_info_dict.get("start_date", "")
            trip_end_str = self.trip_info_dict.get("end_date", "")

            if trip_start_str != "" and trip_end_str != "":
                trip_start_dt = datetime.strptime(trip_start_str, "%d/%m/%Y")
                trip_end_dt = datetime.strptime(trip_end_str, "%d/%m/%Y")

                if expense_dt < trip_start_dt or expense_dt > trip_end_dt:
                    self.show_error(f"Expense date must be within trip period ({trip_start_str} to {trip_end_str})!")
                    return False
        except ValueError:
            self.show_error("Date must be in the format of dd/mm/yyyy.")
            return False

        return True
    
    def confirm_btn_on_click(self):
        '''process input data and append/update expense dictionary in json file'''
        if self.validate_inputs() == False:
            return
        
        title = self.entry_expense_title.get().strip()
        amount_value = float(self.entry_amount.get().replace("$", "").strip())
        date_value = self.entry_date.get().strip()
        category = self.combo_category.get()
        payer = self.combo_payer.get()
        
        selected_members = []
        custom_shares_dict = {}

        if self.manual_split_mode == False:
            for person_name, chk_var in self.checkbox_widget.items():
                if chk_var.get() == True:
                    selected_members.append(person_name)

            if len(selected_members) == 0:
                self.show_error("Please select at least one member to split the expense!")
                return
            
            split_share_amount = amount_value / len(selected_members)
            share_per_person = round(split_share_amount, 2)
        else:
            # Manual split validation
            total_custom_sum = 0.0
            for person_name, entry_box in self.custom_entry_widget.items():
                val_str = entry_box.get().strip().replace("$", "")
                if val_str != "":
                    try:
                        val_num = float(val_str)
                        if val_num > 0:
                            custom_shares_dict[person_name] = val_num
                            total_custom_sum = total_custom_sum + val_num
                            selected_members.append(person_name)
                    except ValueError:
                        self.show_error(f"Invalid custom amount entered for {person_name}!")
                        return

            if abs(total_custom_sum - amount_value) > 0.01:
                self.show_error(f"Sum of custom shares (${total_custom_sum:.2f}) must equal total amount (${amount_value:.2f})!")
                return
            share_per_person = 0.0
        
        expense_dict = {
            "title": title,
            "description": title,
            "amount": amount_value,
            "date": date_value,
            "category": category,
            "payer": payer,
            "split_between": selected_members,
            "custom_shares": custom_shares_dict,
            "share_per_person": share_per_person
        }

        if self.file_path != None and os.path.exists(self.file_path) == True:
            try:
                if "expenses" not in self.trip_info_dict:
                    self.trip_info_dict["expenses"] = []
                    
                if self.edit_item != None and self.edit_item in self.trip_info_dict["expenses"]:
                    idx = self.trip_info_dict["expenses"].index(self.edit_item)
                    self.trip_info_dict["expenses"][idx] = expense_dict
                else:
                    self.trip_info_dict["expenses"].append(expense_dict)

                with open(self.file_path, "w", encoding="utf-8") as file_data:
                    json.dump(self.trip_info_dict, file_data, indent=4)
            except FileNotFoundError:
                self.show_error("Could not find trip file to save changes!")
                return
            
        messagebox.showinfo("Success", f"Expense '{title}' successfully saved!", parent=self.root)

        if self.on_save_callback:
            self.on_save_callback(expense_dict)
