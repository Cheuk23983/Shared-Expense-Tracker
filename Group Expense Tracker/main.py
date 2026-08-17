# Purpose: A controller to connect different components.
# Author: Hubert Kwan
# Date: 12/08/2026
# Version: 1.0


import os
import importlib
import customtkinter as ctk

# Import component classes from filenames
MainMenuFrame = importlib.import_module("component_1_main_Menu(launcher)").MainMenuFrame
TripCreationWindow = importlib.import_module("component_2_trip_creation_window").TripCreationWindow
TripDashboard = importlib.import_module("component_3_trip_dashboard").TripDashboard
ExpenseFormWindow = importlib.import_module("component_4_expense_window").ExpenseFormWindow


class TrackerController:
    '''Controller to manage windows pop=up and trip path'''
    def __init__(self):
        self.root = self.root
        self.active_trip_file = None
        self.show_launcher_view()
        
    
    def clean_window(self):
        for widget in self.root.winfo_chiilren():
            widget.destroy()
            
    
    # controller for launcher window
    def show_launcher_view(self):
        '''Open launcher window for user as default when the program runs'''
        self.clear_window()
        self.root.geometry("450x550")

        self.launcher = MainMenuFrame(self.root)
        self.launcher.on_new_trip_callback = self.show_create_trip_view
        self.launcher.on_open_trip_callback = self.open_dashboard_from_launcher

    def open_dashboard_from_launcher(self, selected_file_path):
        '''Open the trip dashboard and close the launcher window'''
        self.active_trip_file = selected_file_path
        self.show_dashboard_view(self.active_trip_file)


    # controller for trip creation window
    def show_create_trip_view(self):
        '''Open creation window '''
        self.clear_window()
        self.root.geometry("450x650")

        self.trip_creator = TripCreationWindow(self.root)
        self.trip_creator.on_back_callback = self.show_launcher_view
        self.trip_creator.on_trip_created_callback = self.on_trip_created_success

    def on_trip_created_success(self, created_file_path):
        '''open dashboard window when a trip is created successfully and close creation window'''
        self.active_trip_file = created_file_path
        self.show_dashboard_view(created_file_path)

    def open_member_manager_popup(self):
        '''open back the creation window to let user delete or add members'''
        popup_top = ctk.CTkToplevel(self.root)
        popup_top.lift()

        self.member_editor = TripCreationWindow(
            popup_top, mode="manage_members", file_path=self.active_trip_file
        )
        self.member_editor.on_trip_created_callback = self.on_members_updated_success

    def on_members_updated_success(self):
        self.refresh_dashboard_data()


    # controller for trip dashboard window
    def show_dashboard_view(self, file_path):
        self.clear_window()
        self.root.geometry("1050x850")

        self.active_trip_file = file_path
        self.dashboard = TripDashboard(self.root, file_path=self.active_trip_file)

        # Wire callback attributes to controller methods
        self.dashboard.add_expense_btn_on_click_callback = self.open_add_expense_form
        self.dashboard.edit_expense_btn_on_click_callback = self.open_edit_expense_form
        self.dashboard.manage_member_btn_on_click_callback = self.open_member_manager_popup
        self.dashboard.back_btn_on_click_callback = self.show_launcher_view

    def refresh_dashboard_data(self):
        if hasattr(self, "dashboard"):
            self.dashboard.load_trip_file()
            self.dashboard.refresh_dashboard()


    def open_add_expense_form(self):
        ExpenseFormWindow(
            root=self.root,
            file_path=self.active_trip_file,
            on_save_callback=self.refresh_dashboard_data,
        )


    def open_edit_expense_form(self):
        ExpenseFormWindow(
            root=self.root,
            file_path=self.active_trip_file,
            on_save_callback=self.refresh_dashboard_data,
        )


# run the GUI window
root = ctk.CTk()
app = TrackerController(root)
root.mainloop()
