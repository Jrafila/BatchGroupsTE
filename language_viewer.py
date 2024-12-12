import tkinter as tk

def launch_ui():
    # Create the main window
    root = tk.Tk()
    root.title("Language Viewer")

    # Add a button that closes the window
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=20)

    # Run the main loop
    root.mainloop()
