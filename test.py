import json
import tkinter as tk
from tkinter import messagebox, Listbox


def load_languages():
    """Load languages from the JSON file and update the listbox."""
    try:
        with open("languages.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract only the language names (keys)
        languages = list(data.keys())
        
        # Clear the listbox and add languages
        listbox.delete(0, tk.END)
        for lang in languages:
            listbox.insert(tk.END, lang)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load languages: {e}")


# Create the main application window
root = tk.Tk()
root.title("Languages Viewer")
root.geometry("400x300")

# Create a Listbox to display languages
listbox = Listbox(root, width=50, height=15)
listbox.pack(pady=10)

# Create a button to load languages
button = tk.Button(root, text="Load Languages", command=load_languages)
button.pack(pady=10)

# Initial load of languages
load_languages()

# Start the tkinter main loop
root.mainloop()
