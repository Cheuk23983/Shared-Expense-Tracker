# Purpose: A controller to connect different components.
# Author: Hubert Kwan
# Date: 19/08/2026
# Version: 2.0



import os
import importlib
import customtkinter as ctk

# Import component classes dynamically from module filenames
MainMenuFrame = importlib.import_module("component_1_main_menu_launcher").MainMenuFrame
TripCreationWindow = importlib.import_module("component_2_trip_creation_window").TripCreationWindow
TripDashboard = importlib.import_module("component_3_trip_dashboard").TripDashboard
ExpenseFormWindow = importlib.import_module("component_4_expense_window").ExpenseFormWindow


class AppController:
    '''Central controller managing screen transitions and dynamic trip paths'''

    def __init__(self, root):
        self.root = root
        self.active_trip_file = None
        self.show_launcher_view()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            

    # controller for component 
    def show_launcher_view(self):
        self.clear_window()
        self.root.geometry("450x550")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.launcher = MainMenuFrame(self.root)
        self.launcher.on_new_trip_callback = self.show_create_trip_view
        self.launcher.on_open_trip_callback = self.open_dashboard_from_launcher

    def open_dashboard_from_launcher(self, selected_file_path=None):
        self.active_trip_file = selected_file_path
        self.show_dashboard_view(self.active_trip_file)


    # controller for component 2
    def show_create_trip_view(self):
        self.clear_window()
        self.root.geometry("480x700")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.trip_creator = TripCreationWindow(self.root, mode="create_trip", file_path=None)
        self.trip_creator.on_back_callback = self.show_launcher_view
        self.trip_creator.on_trip_created_callback = self.on_trip_created_success

    def on_trip_created_success(self, created_file_path=None):
        self.active_trip_file = created_file_path
        self.show_dashboard_view(created_file_path)

    def open_member_manager_screen(self):
        self.clear_window()
        self.root.geometry("480x700")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.member_editor = TripCreationWindow(
            self.root, mode="manage_members", file_path=self.active_trip_file
        )
        self.member_editor.on_back_callback = lambda: self.show_dashboard_view(self.active_trip_file)
        self.member_editor.on_trip_created_callback = lambda path=None: self.show_dashboard_view(path)

    def open_edit_trip_details_screen(self):
        '''edit trip details mode'''
        self.clear_window()
        self.root.geometry("480x700")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.trip_detail_editor = TripCreationWindow(
            self.root, mode="edit_trip_details", file_path=self.active_trip_file
        )
        self.trip_detail_editor.on_back_callback = lambda: self.show_dashboard_view(self.active_trip_file)
        self.trip_detail_editor.on_trip_created_callback = lambda path=None: self.show_dashboard_view(path)
        
        
    # controller for component 3
    def show_dashboard_view(self, file_path=None):
        self.clear_window()
        self.root.geometry("1200x550")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.active_trip_file = file_path
        self.dashboard = TripDashboard(self.root, file_path=self.active_trip_file)

        # connect callback attributes to controller methods
        self.dashboard.add_expense_btn_on_click_callback = self.open_add_expense_screen
        self.dashboard.edit_expense_btn_on_click_callback = self.open_edit_expense_screen
        self.dashboard.manage_member_btn_on_click_callback = self.open_member_manager_screen
        self.dashboard.edit_trip_details_callback = self.open_edit_trip_details_screen
        self.dashboard.back_btn_on_click_callback = self.show_launcher_view

    def refresh_dashboard_data(self, updated_data=None):
        if hasattr(self, "dashboard") == True:
            self.dashboard.load_trip_file()
            self.dashboard.refresh_dashboard()


    # controller for component 4
    def open_add_expense_screen(self):
        self.clear_window()
        self.root.geometry("480x700")
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
        self.clear_window()
        self.root.geometry("480x700")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.expense_form = ExpenseFormWindow(
            root=self.root,
            file_path=self.active_trip_file,
            on_save_callback=lambda data=None: self.show_dashboard_view(self.active_trip_file),
            on_cancel_callback=lambda: self.show_dashboard_view(self.active_trip_file),
            edit_item=expense_item
        )


if __name__ == "__main__":
    root = ctk.CTk()
    app = AppController(root)
    root.mainloop()
