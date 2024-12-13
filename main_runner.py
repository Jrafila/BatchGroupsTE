import language_viewer
import export_selected_to_excel  # Make sure export_selected_to_excel.py is in the same directory

if __name__ == "__main__":
    language_viewer.launch_ui()  # Runs the GUI and blocks until the user finishes and the window closes
    export_selected_to_excel.export_to_excel()  # Once done, generate the Excel file
