import json
import tkinter as tk
from tkinter import ttk, messagebox
import os

def load_languages():
    """Load languages and their variants from the JSON file."""
    global language_variants
    language_variants = {
        "English": {"US": "en-US", "UK": "en-GB"},
        "German": {"Germany": "de-DE", "Austria": "de-AT"},
        "French": {"France": "fr-FR"}
    }

def update_language_list(search_term):
    """Update the checkboxes based on the search term."""
    pass  # Keep the existing implementation of update_language_list

def update_selected_languages():
    """Update the display of selected languages."""
    pass  # Keep the existing implementation of update_selected_languages

def save_to_json(data):
    """Save the selected languages and variants to a new JSON file."""
    with open('selected_languages.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Languages and variants saved to selected_languages.json.")

def select_variants():
    """Allow the user to select variants one by one."""
    pass  # Keep the existing implementation of select_variants

def on_search_key(event):
    """Handle key release in the search box."""
    pass  # Keep the existing implementation of on_search_key

def main():
    """Main function to run the language viewer."""
    is_ci = os.getenv('CI', False)  # Check if running in GitHub Actions or non-interactive environment

    if is_ci:
        print("Running in CI environment, skipping UI.")
        load_languages()
        selected_languages = {"German": {"Germany": "de-DE", "Austria": "de-AT"}}
        save_to_json(selected_languages)
        print("Languages processed and saved.")
    else:
        global root
        root = tk.Tk()
        root.title("Languages Viewer")
        root.geometry("800x500")

        # Search box
        search_var = tk.StringVar()
        search_box = tk.Entry(root, textvariable=search_var, width=40)
        search_box.pack(pady=10)
        search_box.bind("<KeyRelease>", on_search_key)

        # Main frames
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable language frame
        language_canvas = tk.Canvas(main_frame, width=300, height=300)
        language_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=language_canvas.yview)
        language_canvas.configure(yscrollcommand=language_scrollbar.set)

        language_scrollbar.pack(side="left", fill="y")
        language_canvas.pack(side="left", fill="both", expand=True)

        language_frame_inner = ttk.Frame(language_canvas)
        language_canvas.create_window((0, 0), window=language_frame_inner, anchor="nw")

        # Scrollable selected languages frame
        selected_canvas = tk.Canvas(main_frame, width=300, height=300, bg="lightgray")
        selected_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=selected_canvas.yview)
        selected_canvas.configure(yscrollcommand=selected_scrollbar.set)

        selected_scrollbar.pack(side="right", fill="y")
        selected_canvas.pack(side="right", fill="both", expand=True)

        selected_frame_inner = tk.Frame(selected_canvas, bg="lightgray")
        selected_canvas.create_window((0, 0), window=selected_frame_inner, anchor="nw")

        tk.Label(selected_frame_inner, text="Selected Languages", bg="lightgray", font=("Arial", 12, "bold")).pack(pady=5)

        # Button to select variants
        variant_button = tk.Button(root, text="Select Variants", command=select_variants)
        variant_button.pack(pady=10)

        # Load languages
        all_languages = []  # To store the full list of languages
        language_vars = {}  # To track the state of each checkbox
        language_variants = {}  # To store language variants
        load_languages()

        # Start the tkinter main loop
        root.protocol("WM_DELETE_WINDOW", root.quit)  # Ensure the window closes cleanly
        root.mainloop()  # Run the tkinter main event loop

if __name__ == "__main__":
    main()
