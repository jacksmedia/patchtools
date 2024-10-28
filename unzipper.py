import zipfile
import os

# Set the directory containing your .zip files and the output directory
directory_with_zips = '.'  # Replace with the folder containing your zip files
output_directory = './a-fresh-batch'  # Replace with your desired output folder

# Function to unzip files and rename .sfc files
def unzip_and_rename_sfc(directory_with_zips, output_dir):
    for zip_filename in os.listdir(directory_with_zips):
        if zip_filename.endswith(".zip"):
            zip_path = os.path.join(directory_with_zips, zip_filename)
            zip_name = os.path.splitext(zip_filename)[0]  # Get the name of the zip without the extension
            
            # Create a directory named after the zip file
            unzip_dir = os.path.join(output_dir, zip_name)
            os.makedirs(unzip_dir, exist_ok=True)
            
            # Unzip into the newly created directory
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(unzip_dir)
                print(f"Extracted {zip_filename} to {unzip_dir}")
                
            # Rename any .sfc files inside the unzipped directory
            for root, dirs, files in os.walk(unzip_dir):
                for file in files:
                    if file.endswith(".sfc"):
                        old_file_path = os.path.join(root, file)
                        new_file_name = f"{zip_name}.sfc"  # Rename .sfc file to match the zip name
                        new_file_path = os.path.join(root, new_file_name)
                        os.rename(old_file_path, new_file_path)
                        print(f"Renamed {file} to {new_file_name} in {unzip_dir}")

# Example usage:
unzip_and_rename_sfc(directory_with_zips, output_directory)
