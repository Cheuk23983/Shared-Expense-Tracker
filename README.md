# Group Expense Tracker & Settlement
Have you ever struggled when it comes to paying bills within a friend group? Group Expense Tracker is a modern desktop application built in Python using the tkinter module that simplifies tracking shared trip expenses, managing group balance and tracking barriers to owning money. 
## Project Overview
When travelling with friends or family, tracking who paid for what and calculating who owes whom can become complex and messy. This application solves that problem by allowing users to manage trips, log multi-currency expenses, filter past transactions, and generate automated, Excel-compatible settlement reports. Built with an **Object-Oriented Programming (OOP)** architecture following a clean **Model-View-Controller (MVC)** design pattern, the system keeps mathematical logic strictly separated from the presentation layer while prioritising defensive data validation and local privacy.
## Key Features
* **Trip & Member Management:** Create, view, and manage individual trip files with customizable participant rosters.
* **Batch Operations:** Multi-select and delete old or unnecessary trip files directly from the launcher dashboard.
* **Dynamic Search & Filtering:** Filter trip ledgers in real-time by category, date, or search keywords.
* **Flexible Cost Allocation:** Support for both **Equal Splits** and custom **Percentage Splits**.
* **Debt-Simplification Solver:** An optimised algorithm that calculates net positions ($Payments - Expenses$) and pairs maximum debtors with maximum creditors to minimise overall repayment transactions.
## Built with
* **Language:** Python3.11
* **GUI Framework:** CustomTkinter
*  **Data Storage:** JSON File(Store locally)
## Getting Started
### Device Requirements
* Ensure you have Python 3.11 or higher installed on your system.
* You can verify this by running the command in the terminal:
  ```bash
  python --version
* Ensure the customtkinter module is installed.
