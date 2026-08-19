# Purpose: Component 5 is to display detailed read-only information for a selected transaction in a pop-up window.
# Author: Hubert Kwan
# Date: 20/08/2026
# Version: 1.0

# Import required libraries and modules
import customtkinter as ctk

# UI Theme Color Constants
COLOR_EDIT_BTN = "#1F6AA5"
COLOR_CLOSE_BTN = "gray"
COLOR_CLOSE_HOVER_BTN = "#555555"

# Set up app appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class TransactionDetailWindow:
    '''Pop-up window class to display expense details in read-only view'''
    def __init__(self, root, expense_item=None, on_edit_callback=None, on_close_callback=None):
        self.root = root
        self.expense_item = expense_item
        self.on_edit_callback = on_edit_callback
        self.on_close_callback = on_close_callback

        if self.expense_item == None:
            self.expense_item = {}

        # Configure pop-up top-level window properties
        self.top = ctk.CTkToplevel(self.root)
        self.top.title("Transaction Detail Window")
        self.top.geometry("400x500")
        self.top.lift()
        self.top.grab_set()

        # Grid configuration
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)

        # Build window widgets
        self.create_widgets()

    def create_widgets(self):
        '''Build all labels and display widgets matching conceptual design'''
        # Header title
        self.lbl_header = ctk.CTkLabel(self.top, text="Transaction Detail Window", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_header.grid(row=0, column=0, columnspan=2, pady=(15, 10))

        # Expense Title Display Card
        expense_title = self.expense_item.get("title", self.expense_item.get("description", "Unnamed Expense"))
        self.title_card = ctk.CTkFrame(self.top, corner_radius=8)
        self.title_card.grid(row=1, column=0, columnspan=2, padx=20, pady=6, sticky="ew")

        self.lbl_title_val = ctk.CTkLabel(self.title_card, text=expense_title, font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_title_val.pack(pady=10)

        # Side-by-side cards displaying Payer Name and Total Amount Paid
        payer_name = self.expense_item.get("payer", "N/A")
        total_amount = self.expense_item.get("amount", 0.0)

        self.payer_card = ctk.CTkFrame(self.top, corner_radius=8)
        self.payer_card.grid(row=2, column=0, padx=(20, 5), pady=6, sticky="ew")

        self.lbl_payer_val = ctk.CTkLabel(self.payer_card, text=f"Payer: {payer_name}", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_payer_val.pack(pady=10)

        self.amount_card = ctk.CTkFrame(self.top, corner_radius=8)
        self.amount_card.grid(row=2, column=1, padx=(5, 20), pady=6, sticky="ew")

        self.lbl_amount_val = ctk.CTkLabel(self.amount_card, text=f"Amount: ${total_amount:.2f}", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_amount_val.pack(pady=10)

        # Container card for detailed breakdown per group member
        self.split_card = ctk.CTkFrame(self.top, corner_radius=10)
        self.split_card.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        self.lbl_split_title = ctk.CTkLabel(self.split_card, text="Detailed Splitting Breakdown", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_split_title.pack(pady=(10, 5))

        self.scroll_breakdown = ctk.CTkScrollableFrame(self.split_card, fg_color="transparent", height=150)
        self.scroll_breakdown.pack(fill="both", expand=True, padx=10, pady=5)

        # Display individual share line items per member based on split type
        split_members = self.expense_item.get("split_between", [])
        custom_shares = self.expense_item.get("custom_shares", {})
        share_per_person = self.expense_item.get("share_per_person", 0.0)

        # Display custom shares if custom splitting dictionary was saved
        if len(custom_shares) > 0:
            for person, share in custom_shares.items():
                row_frame = ctk.CTkFrame(self.scroll_breakdown, fg_color="transparent")
                row_frame.pack(fill="x", pady=2)

                lbl_person = ctk.CTkLabel(row_frame, text=f"{person}:", font=ctk.CTkFont(size=13))
                lbl_person.pack(side="left", padx=10)

                lbl_val = ctk.CTkLabel(row_frame, text=f"${share:.2f}", font=ctk.CTkFont(size=13, weight="bold"))
                lbl_val.pack(side="right", padx=10)
        else:
            # Fallback calculation for equal split shares
            if share_per_person == 0.0 and len(split_members) > 0:
                share_per_person = round(total_amount / len(split_members), 2)

            for person in split_members:
                row_frame = ctk.CTkFrame(self.scroll_breakdown, fg_color="transparent")
                row_frame.pack(fill="x", pady=2)

                lbl_person = ctk.CTkLabel(row_frame, text=f"{person}:", font=ctk.CTkFont(size=13))
                lbl_person.pack(side="left", padx=10)

                lbl_val = ctk.CTkLabel(row_frame, text=f"${share_per_person:.2f}", font=ctk.CTkFont(size=13, weight="bold"))
                lbl_val.pack(side="right", padx=10)

        # Action Buttons to change to to edit mode or close window
        self.btn_edit = ctk.CTkButton(self.top, text="Pivot to Edit Mode", fg_color=COLOR_EDIT_BTN, command=self.pivot_to_edit_click)
        self.btn_edit.grid(row=4, column=0, padx=(20, 5), pady=(10, 15), sticky="ew")

        self.btn_close = ctk.CTkButton(self.top, text="Close", fg_color=COLOR_CLOSE_BTN, hover_color=COLOR_CLOSE_HOVER_BTN, command=self.close_click)
        self.btn_close.grid(row=4, column=1, padx=(5, 20), pady=(10, 15), sticky="ew")

    def pivot_to_edit_click(self):
        '''Destroys pop-up and triggers callback to open expense form in edit mode'''
        self.top.destroy()
        if self.on_edit_callback:
            self.on_edit_callback(self.expense_item)

    def close_click(self):
        '''Destroys pop-up window'''
        self.top.destroy()
        if self.on_close_callback:
            self.on_close_callback()
