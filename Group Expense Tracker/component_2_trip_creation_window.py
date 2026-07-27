# Purpose: This program is to create a window for user to create a tirp JSON file to add expenses.
# Author: Hubert Kwan
# Date: 27/07/2026
# Version: 1.0


# import libraries and modules
import customtkinter as ctk
import json
import os
from tkinter import messagebox

# create class for trip creation
class TripCreationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Trip Creation Window")
        self.root.geometry("450x550")
