import tkinter as tk
import os

def on_button_click():
    """Handler for the button click, closes the window."""
    print("Button clicked, closing the window.")
    root.quit()  # Closes the tkinter window

# Check if running in CI (GitHub Actions)
is_ci = os.getenv('CI', False)  # GitHub Actions sets 'CI' to True by default

if is_ci:
    print("Running in CI environment, skipping the UI and closing immediately.")
    # Simulate the behavior in CI (by skipping the GUI and immediately closing)
    # Simulate the button click behavior by calling the function directly
    on_button_click()
else:
    # Create the main application window for local environments (interactive)
    root = tk.Tk()
    root.title("Simple UI")
    root.geometry("300x200")

    # Add a button that closes the window when clicked
    button = tk.Button(root, text="Click to Close", command=on_button_click)
    button.pack(pady=50)

    # Start the tkinter main loop (wait for user interaction)
    root.mainloop()
