import os
import sys
import json
from openpyxl import Workbook

def export_to_excel():
    # Base directory where the exe and selected.json reside
    base_dir = os.path.dirname(sys.executable)
    json_path = os.path.join(base_dir, "selected.json")

    if not os.path.exists(json_path):
        print("No selected.json file found. Please run the selection process first.")
        return

    # Load the selected languages and codes
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create a new Excel workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Selected Languages"

    # Write header row
    ws.append(["Language", "Code"])

    # Write each selected language and its code
    for language, code in data.items():
        ws.append([language, code])

    # Save the workbook
    excel_filename = "selected_languages.xlsx"
    excel_path = os.path.join(base_dir, excel_filename)
    wb.save(excel_path)
    print(f"Excel file created: {excel_path}")

if __name__ == "__main__":
    export_to_excel()
