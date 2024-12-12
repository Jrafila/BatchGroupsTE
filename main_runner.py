import subprocess
import sys

def run_script(script_name):
    """Run a script without showing a console window and wait for it to complete."""
    print(f"Starting {script_name}...")
    
    # Suppress the console window on Windows
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    result = subprocess.run(
        [sys.executable, script_name],
        startupinfo=si
    )
    
    if result.returncode != 0:
        print(f"Error running {script_name}. Exiting.")
        sys.exit(result.returncode)  # Exit if a script fails
    print(f"Finished {script_name}.")

def main():
    print("Starting the process...")

    # Step 1: Run the language viewer script
    run_script("language_viewer.py")

    print("All scripts executed successfully.")

if __name__ == "__main__":
    main()
