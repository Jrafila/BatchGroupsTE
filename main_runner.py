import subprocess
import sys

def run_script(script_name):
    """Run a script and wait for it to complete."""
    print(f"Starting {script_name}...")

    # Run the script (no console window suppression for simplicity here)
    result = subprocess.run([sys.executable, script_name])

    if result.returncode != 0:
        print(f"Error running {script_name}. Exiting.")
        sys.exit(result.returncode)  # Exit if a script fails
    print(f"Finished {script_name}.")

def main():
    print("Starting the process...")

    # Run the language viewer script (UI part)
    run_script("language_viewer.py")

    print("All scripts executed successfully.")

if __name__ == "__main__":
    main()
