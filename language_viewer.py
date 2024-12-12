import tkinter as tk

def on_button_click():
    """Handler for the button click, closes the window."""
    print("Button clicked, closing the window.")
    root.quit()  # Closes the tkinter window

# Create the main application window
root = tk.Tk()
root.title("Simple UI")
root.geometry("300x200")

# Add a button that closes the window when clicked
button = tk.Button(root, text="Click to Close", command=on_button_click)
button.pack(pady=50)

# Start the tkinter main loop (wait for user interaction)
root.mainloop()
