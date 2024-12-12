import tkinter as tk
from tkinter import messagebox

def on_button_click():
    # Action performed when the button is clicked
    messagebox.showinfo("Button Clicked", "You clicked the button!")

# Create the main application window
root = tk.Tk()
root.title("Simple UI")

# Set the size of the window
root.geometry("300x200")

# Create a button and add it to the window
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=20)  # Adds some vertical spacing

# Start the tkinter main loop
root.mainloop()
