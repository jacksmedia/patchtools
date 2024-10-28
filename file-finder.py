import os
import shutil

# Set the directory where you want to search for the files
search_directory = '.'  # Replace with your starting directory
file_extension = '.sfc'  # Change this to the file type you are looking for

# Function to search for files and copy them to the current directory
def copy_files_to_current_dir(search_dir, extension):
    current_dir = os.getcwd()  # Get the current directory where the script is running
    
    for foldername, subfolders, filenames in os.walk(search_dir):
        for filename in filenames:
            if filename.endswith(extension):
                source_file_path = os.path.join(foldername, filename)
                destination_file_path = os.path.join(current_dir, filename)
                
                # Copy the file to the current directory
                shutil.copy2(source_file_path, destination_file_path)
                print(f"Copied {filename} to {current_dir}")

# Example usage:
copy_files_to_current_dir(search_directory, file_extension)