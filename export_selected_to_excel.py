import os
import sys
import json
from openpyxl import Workbook
import tkinter as tk
from tkinter import simpledialog

def get_customer_info():
    """
    Display a simple UI to get customer name and location from the user.
    Returns:
        dict: Dictionary containing 'Customer Name' and 'Customer Location'.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Get inputs from the user
    customer_name = simpledialog.askstring("Input", "Enter Customer Name:", parent=root)
    customer_location = simpledialog.askstring("Input", "Enter Customer Location:", parent=root)

    root.destroy()  # Destroy the root window

    return {"Customer Name": customer_name, "Customer Location": customer_location}


def export_to_excel():
    try:
        # Base directory where the exe and selected.json reside
        base_dir = os.path.dirname(sys.executable)
        json_path = os.path.join(base_dir, "selected.json")

        # Debugging: print directory and file being checked
        print(f"Looking for selected.json in: {base_dir}")
        print(f"Full path to JSON: {json_path}")

        if not os.path.exists(json_path):
            print("No selected.json file found. Please run the selection process first.")
            return 1

        # Load the selected languages and codes
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Get customer information from the user
        customer_info = get_customer_info()

        # Create a new Excel workbook and worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Selected Languages"

        # Define headers: "Name", "Description", "Location", "Role"
        headers = ["Name", "Description", "Location", "Role"]
        ws.append(headers)

        # Populate the first row with customer info and consolidated roles
        name = customer_info.get("Customer Name", "N/A")
        location = customer_info.get("Customer Location", "N/A")
        description = "Customer Language Preferences"
        role = ", ".join(data.keys())  # Consolidate all selected languages into a single string

        # Write the first row
        row = [name, description, location, role]
        ws.append(row)

        # Save the workbook
        excel_filename = "selected_languages.xlsx"
        excel_path = os.path.join(base_dir, excel_filename)
        wb.save(excel_path)
        print(f"Excel file created: {excel_path}")

        # Delete the selected.json file
        try:
            os.remove(json_path)
            print(f"Deleted intermediate file: {json_path}")
        except Exception as e:
            print(f"Error deleting {json_path}: {e}")
            return 1

        print("Process completed successfully.")
        return 0

    except Exception as e:
        print(f"An error occurred: {e}")
        return 1


if __name__ == "__main__":
    exit_code = export_to_excel()
    sys.exit(exit_code)
