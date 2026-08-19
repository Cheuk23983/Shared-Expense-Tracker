# Purpose: The Main program is the controller to link bewteen component 1 to component 5. This allow switching screen seemlessly from onw to another.
# Author: Hubert Kwan
# Date: 20/08/2026
# Version: 2.1

# Import required libraries and modules
import importlib
import os
import customtkinter as ctk

# Window Dimension Constants
WINDOW_SIZE_LAUNCHER = (450, 550)
WINDOW_SIZE_FORM = (480, 700)
WINDOW_SIZE_DASHBOARD = (1200, 550)

# import individual component GUI window classes from their Python files
MainMenuFrame = importlib.import_module("component_1_main_menu_launcher").MainMenuFrame
TripCreationWindow = importlib.import_module("component_2_trip_creation_window").TripCreationWindow
TripDashboard = importlib.import_module("component_3_trip_dashboard").TripDashboard
ExpenseFormWindow = importlib.import_module("component_4_expense_window").ExpenseFormWindow
TransactionDetailWindow = importlib.import_module("component_5_transaction_detail").TransactionDetailWindow


class AppController:
    '''Central controller managing screen transitions and dynamic trip paths'''

    def __init__(self, root):
        # initialize app flow on the launcher screen
        self.root = root
        self.active_trip_file = None
        self.show_launcher_view()

    def clear_window(self):
        '''Destroys all existing widgets and resets grid weight configurations'''
        # Remove active child widgets from current screen
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Reset grid weights so layout does not stretch incorrectly when switching views
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=0)
            self.root.grid_rowconfigure(i, weight=0)

    def set_window_size(self, width, height):
        '''Forces Tkinter to update pending tasks before applying new geometry dimensions'''
        self.clear_window()
        self.root.update_idletasks()
        self.root.geometry(f"{width}x{height}")

    # Component 1 (launcher)
    def show_launcher_view(self):
        # Resize window and display Component 1 launcher menu
        self.set_window_size(WINDOW_SIZE_LAUNCHER[0], WINDOW_SIZE_LAUNCHER[1])
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.launcher = MainMenuFrame(self.root)
        self.launcher.on_new_trip_callback = self.show_create_trip_view
        self.launcher.on_open_trip_callback = self.open_dashboard_from_launcher

    def open_dashboard_from_launcher(self, selected_file_path=None):
        # Store active selected file path and route to dashboard view
        self.active_trip_file = selected_file_path
        self.show_dashboard_view(self.active_trip_file)

    # Component 2 (Trip Creation Window)
    def show_create_trip_view(self):
        # Resize window and show trip creation view
        self.set_window_size(WINDOW_SIZE_FORM[0], WINDOW_SIZE_FORM[1])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.trip_creator = TripCreationWindow(self.root, mode="create_trip", file_path=None)
        self.trip_creator.on_back_callback = self.show_launcher_view
        self.trip_creator.on_trip_created_callback = self.on_trip_created_success

    def on_trip_created_success(self, created_file_path=None):
        # Callback when trip creation succeeds
        self.active_trip_file = created_file_path
        self.show_dashboard_view(created_file_path)

    def open_member_manager_screen(self):
        # Show member management mode screen for the active trip
        self.set_window_size(WINDOW_SIZE_FORM[0], WINDOW_SIZE_FORM[1])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.member_editor = TripCreationWindow(
            self.root, mode="manage_members", file_path=self.active_trip_file
        )
        self.member_editor.on_back_callback = lambda: self.show_dashboard_view(self.active_trip_file)
        self.member_editor.on_trip_created_callback = lambda path=None: self.show_dashboard_view(path)

    def open_edit_trip_details_screen(self):
        # Show trip details editing mode screen
        self.set_window_size(WINDOW_SIZE_FORM[0], WINDOW_SIZE_FORM[1])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.trip_detail_editor = TripCreationWindow(
            self.root, mode="edit_trip_details", file_path=self.active_trip_file
        )
        self.trip_detail_editor.on_back_callback = lambda: self.show_dashboard_view(self.active_trip_file)
        self.trip_detail_editor.on_trip_created_callback = lambda path=None: self.show_dashboard_view(path)

    # Component 3(Trip Dashboard) & Component 5(Transaction detail)
    def show_dashboard_view(self, file_path=None):
        # Resize window to wide format and render main trip dashboard
        self.set_window_size(WINDOW_SIZE_DASHBOARD[0], WINDOW_SIZE_DASHBOARD[1])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.active_trip_file = file_path
        self.dashboard = TripDashboard(self.root, file_path=self.active_trip_file)

        # Connect callback attributes to controller methods
        self.dashboard.add_expense_btn_on_click_callback = self.open_add_expense_screen
        self.dashboard.edit_expense_btn_on_click_callback = self.open_edit_expense_screen
        self.dashboard.view_expense_detail_callback = self.open_transaction_detail_popup
        self.dashboard.manage_member_btn_on_click_callback = self.open_member_manager_screen
        self.dashboard.edit_trip_details_callback = self.open_edit_trip_details_screen
        self.dashboard.back_btn_on_click_callback = self.show_launcher_view

    def open_transaction_detail_popup(self, expense_item=None):
        '''Opens Component 5 Pop-up Window to view expense breakdown'''
        # Instantiate component 5 popup window
        self.detail_popup = TransactionDetailWindow(
            root=self.root,
            expense_item=expense_item,
            on_edit_callback=self.open_edit_expense_screen,
            on_close_callback=None
        )

    # -Component 4 (Expense Form)
    def open_add_expense_screen(self):
        # Show expense form window in 'add' mode
        self.set_window_size(WINDOW_SIZE_FORM[0], WINDOW_SIZE_FORM[1])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.expense_form = ExpenseFormWindow(
            root=self.root,
            file_path=self.active_trip_file,
            on_save_callback=lambda data=None: self.show_dashboard_view(self.active_trip_file),
            on_cancel_callback=lambda: self.show_dashboard_view(self.active_trip_file),
            edit_item=None
        )

    def open_edit_expense_screen(self, expense_item=None):
        # Show expense form window pre-filled in 'edit' mode
        self.set_window_size(WINDOW_SIZE_FORM[0], WINDOW_SIZE_FORM[1])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.expense_form = ExpenseFormWindow(
            root=self.root,
            file_path=self.active_trip_file,
            on_save_callback=lambda data=None: self.show_dashboard_view(self.active_trip_file),
            on_cancel_callback=lambda: self.show_dashboard_view(self.active_trip_file),
            edit_item=expense_item
        )


# initialise ctk window application
root = ctk.CTk()
app = AppController(root)
root.mainloop()
