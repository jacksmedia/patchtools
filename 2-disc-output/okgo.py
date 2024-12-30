import os
import subprocess

# Define the reference file (update this path if necessary)
REFERENCE_FILE = "2bpp-lookup.tbl"

# Function to del existing output files
def delete_existing_output_files():
    for file in os.listdir():
        if file.endswith("-output.txt"):
            try:
                os.remove(file)
                print(f"Deleted previous output file: {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")

# Function to process all .txt files in the current directory
def run_script_for_txt_files():
    # Get all .txt files in the current working directory
    txt_files = [f for f in os.listdir() if f.endswith(".txt")]
    
    for txt_file in txt_files:
        # Construct the output file name
        output_file = txt_file.replace(".txt", "-output.txt")
        
        # Build the command
        command = ["python", "translator.py", txt_file, REFERENCE_FILE, output_file]
        
        try:
            # Run the command
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Processed {txt_file} -> {output_file}")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {txt_file}: {e.stderr}")

if __name__ == "__main__":
    delete_existing_output_files() # remove old output
    run_script_for_txt_files() # create fresh output
