import subprocess

# List of Python scripts to run
script_list = [
    "1multipatcher.py",
    "2multipatcher.py",
    "3multipatcher.py",
    "4multipatcher.py",
    "5multipatcher.py",
    "6multipatcher.py",
    "7multipatcher.py",
    "8multipatcher.py",
    "9multipatcher.py",
    "Xmultipatcher.py"
]

def run_scripts_sequentially(scripts):
    for script in scripts:
        try:
            print(f"Running {script}...")
            result = subprocess.run(["python", script], check=True)
            print(f"{script} completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {script}: {e}")
        except Exception as e:
            print(f"Unexpected error with {script}: {e}")

# Run the scripts
run_scripts_sequentially(script_list)
