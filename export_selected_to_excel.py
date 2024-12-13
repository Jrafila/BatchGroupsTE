import os
import sys
import json
from openpyxl import Workbook
import tkinter as tk

def get_customer_info():
    """
    Display a single UI to get customer name, location, and checkboxes
    for LO, CR, and PJM groups.
    Returns:
        (customer_name, customer_location, lo_selected, cr_selected, pjm_selected)
    """
    root = tk.Tk()
    root.title("Customer Information")

    # Center the window on the screen
    root.update_idletasks()
    w = 300
    h = 250
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # Customer Name
    tk.Label(root, text="Customer Name:").pack(pady=(10,0))
    name_var = tk.StringVar()
    name_entry = tk.Entry(root, textvariable=name_var)
    name_entry.pack(pady=5)

    # Customer Location
    tk.Label(root, text="Customer Location:").pack(pady=(10,0))
    location_var = tk.StringVar()
    location_entry = tk.Entry(root, textvariable=location_var)
    location_entry.pack(pady=5)

    # Checkboxes for LO, CR, PJM
    lo_var = tk.BooleanVar(value=False)
    cr_var = tk.BooleanVar(value=False)
    pjm_var = tk.BooleanVar(value=False)

    tk.Checkbutton(root, text="Create LO Groups", variable=lo_var).pack(anchor="w", padx=10)
    tk.Checkbutton(root, text="Create CR Groups", variable=cr_var).pack(anchor="w", padx=10)
    tk.Checkbutton(root, text="Create PJM Group", variable=pjm_var).pack(anchor="w", padx=10)

    def on_ok():
        # On OK, just close the dialog
        root.destroy()

    ok_button = tk.Button(root, text="Create Template", command=on_ok)
    ok_button.pack(pady=10)

    root.mainloop()

    customer_name = name_var.get().strip()
    customer_location = location_var.get().strip()
    lo_selected = lo_var.get()
    cr_selected = cr_var.get()
    pjm_selected = pjm_var.get()

    return customer_name, customer_location, lo_selected, cr_selected, pjm_selected


def export_to_excel():
    try:
        # Base directory where the exe and selected.json reside
        base_dir = os.path.dirname(sys.executable)
        json_path = os.path.join(base_dir, "selected.json")

        print(f"Looking for selected.json in: {base_dir}")
        print(f"Full path to JSON: {json_path}")

        if not os.path.exists(json_path):
            print("No selected.json file found. Please run the selection process first.")
            return 1

        # Load the selected languages and codes
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # data format: { "English": "en-US", "Spanish": "es-ES", ... }

        # Get customer info and checkbox selections
        customer_name, customer_location, lo_selected, cr_selected, pjm_selected = get_customer_info()

        # Create a new Excel workbook and worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Selected Languages"

        # Headers
        headers = ["Name", "Description", "Location", "Role"]
        ws.append(headers)

        # For LO and CR groups: create rows for each selected language
        for full_language_name, code in data.items():
            # LO Groups
            if lo_selected:
                name_cell = f"{customer_name} {code} LO Group"
                description_cell = f"{customer_name} {full_language_name} LO Group"
                location_cell = customer_location
                role_cell = "RWS Lead Translator"
                ws.append([name_cell, description_cell, location_cell, role_cell])

            # CR Groups
            if cr_selected:
                name_cell = f"{customer_name} {code} CR Group"
                description_cell = f"{customer_name} {full_language_name} CR Group"
                location_cell = customer_location
                role_cell = "Customer Reviewer"
                ws.append([name_cell, description_cell, location_cell, role_cell])

        # PJM Group: Only 1 row total, no language info
        if pjm_selected:
            name_cell = f"{customer_name} RWS PJM Group"
            description_cell = f"{customer_name} RWS PJM Group"
            location_cell = customer_location
            role_cell = "Project Manager"
            ws.append([name_cell, description_cell, location_cell, role_cell])

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
