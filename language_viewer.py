import tkinter as tk
import os
import time

def on_button_click():
    """Handler for the button click, closes the window."""
    print("Button clicked, closing the window.")
    root.quit()  # Closes the tkinter window

# Check if running in CI (GitHub Actions)
is_ci = os.getenv('CI', False)  # GitHub Actions sets 'CI' to True by default

# Track the flow of execution for debugging
print("Starting language_viewer.py...")

# Create the main application window even in CI
root = tk.Tk()

if is_ci:
    print("Running in CI environment, skipping the UI and closing immediately.")
    # Simulate the behavior in CI (by skipping the GUI and immediately closing)
    # Simulate the button click behavior by calling the function directly
    on_button_click()  # Simulate button click to close the window immediately
else:
    # Create the main application window for local environments (interactive)
    print("Running in interactive mode, showing the GUI.")
    root.title("Simple UI")
    root.geometry("300x200")

    # Add a button that closes the window when clicked
    button = tk.Button(root, text="Click to Close", command=on_button_click)
    button.pack(pady=50)

    try:
        # Start the tkinter main loop (wait for user interaction)
        root.mainloop()
    except Exception as e:
        print(f"Error with tkinter mainloop: {e}")
        root.quit()  # Ensure the window closes if something goes wrong

# End of language_viewer.py
print("Exiting language_viewer.py.")
