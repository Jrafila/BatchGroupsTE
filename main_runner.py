import subprocess
import sys
import os

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

    # Check if the script is running in GitHub Actions or another CI environment
    is_ci = os.getenv('CI', False)  # GitHub Actions sets 'CI' to True by default
    
    if is_ci:
        print("Running in CI environment, skipping UI.")
        # Run the logic directly without the UI part
        # For instance, simulate language selection and saving data to a JSON file
        subprocess.run([sys.executable, "language_viewer.py"])  # This will run the logic in a non-interactive way
    else:
        # Step 1: Run the language viewer script with the GUI (for local environments)
        run_script("language_viewer.py")

    print("All scripts executed successfully.")

if __name__ == "__main__":
    main()
