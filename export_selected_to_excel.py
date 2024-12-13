import os
import sys
import json
from openpyxl import Workbook
import tkinter as tk

def get_customer_info():
    """
    Display a single UI to get both customer name and location from the user.
    Returns:
        (customer_name, customer_location): Both strings as entered by the user.
    """
    # Create a custom dialog window
    root = tk.Tk()
    root.title("Customer Information")

    # Center the window on the screen
    root.update_idletasks()
    w = 300
    h = 200
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text="Customer Name:").pack(pady=(10,0))
    name_var = tk.StringVar()
    name_entry = tk.Entry(root, textvariable=name_var)
    name_entry.pack(pady=5)

    tk.Label(root, text="Customer Location:").pack(pady=(10,0))
    location_var = tk.StringVar()
    location_entry = tk.Entry(root, textvariable=location_var)
    location_entry.pack(pady=5)

    # We'll store the inputs and close the window on OK
    def on_ok():
        root.quit()

    ok_button = tk.Button(root, text="OK", command=on_ok)
    ok_button.pack(pady=10)

    # Wait for user input
    root.mainloop()

    # Get values before destroying the root
    customer_name = name_var.get().strip()
    customer_location = location_var.get().strip()

    root.destroy()
    return customer_name, customer_location

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

        # Get customer information from the user (single window)
        customer_name, customer_location = get_customer_info()

        # Create a new Excel workbook and worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Selected Languages"

        # Headers
        headers = ["Name", "Description", "Location", "Role"]
        ws.append(headers)

        # For each selected language in data, create one row
        # data: {full_language_name: code}
        # Name = CustomerName + code + LO Group
        # Description = CustomerName + full_language_name + LO Group
        # Location = user input location
        # Role = RWS Lead Translator
        for full_language_name, code in data.items():
            name_cell = f"{customer_name} {code} LO Group"
            description_cell = f"{customer_name} {full_language_name} LO Group"
            location_cell = customer_location
            role_cell = "RWS Lead Translator"

            row = [name_cell, description_cell, location_cell, role_cell]
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
