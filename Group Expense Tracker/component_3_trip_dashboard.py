# Purpose: This part of the component is to display detail of a chosen trip on the launcher, like the transactions, settlement, and member balance etc.
# Author: Hubert Kwan
# Date: 04/08/2026
# Version: 1.0


# import libraries and modules
import os
import json
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox


class TripDashboard:
    def __init__(self, root, file_path=None):
        self.root = root
        self.root.title("Trip Dashboard")
        self.root.geometry("650x850")

