import subprocess
import sys
import time

def run_script(script_name):
    """Run a script once and wait for it to complete."""
    print(f"Starting {script_name}...")

    try:
        result = subprocess.run([sys.executable, script_name], check=True)  # 'check=True' raises an error on non-zero return code

        if result.returncode != 0:
            print(f"Error running {script_name}. Exiting.")
            sys.exit(result.returncode)  # Exit if a script fails
        print(f"Finished {script_name}.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        sys.exit(e.returncode)  # Exit with the error code

    except Exception as e:
        print(f"Unexpected error running {script_name}: {e}")
        sys.exit(1)  # Exit with generic error code

def main():
    print("Starting the process...")

    try:
        # Run the language viewer script (UI part) only once
        run_script("language_viewer.py")
        print("All scripts executed successfully.")
    
    except Exception as e:
        print(f"An error occurred during the execution of main_runner.py: {e}")

if __name__ == "__main__":
    main()
