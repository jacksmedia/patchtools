import os
import ips

# Function to generate an IPS patch
def create_ips_patch(original_rom, modified_rom, output_patch):
    try:
        # Load original and modified ROMs
        with open(original_rom, 'rb') as orig, open(modified_rom, 'rb') as mod:
            # Generate the patch using the 'ips' library
            patch = ips.Patch.create(orig, mod)

        # Save the IPS patch
        with open(output_patch, 'wb') as patch_file:
            patch_file.write(bytes(patch))  # writes using bytes method

        print(f"Patch file '{output_patch}' created successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to loop through the directory and create patches for each .sfc file
def batch_patch_directory(original_rom, roms_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Loop through all files in the roms_directory
    for filename in os.listdir(roms_directory):
        if filename.endswith(".sfc"):  # Only process .sfc files
            modified_rom = os.path.join(roms_directory, filename)
            
            # Define the output patch file path
            patch_name = os.path.splitext(filename)[0] + ".ips"  # Change .sfc to .ips
            output_patch = os.path.join(output_directory, patch_name)

            # Create the patch for each ROM
            create_ips_patch(original_rom, modified_rom, output_patch)

# Example usage
original_rom = './_improved-rom.sfc'  # Path to the original ROM
roms_directory = './modified_roms'  # Directory containing modified ROMs
output_directory = './fresh-style-packs'  # Directory to save the patch files

batch_patch_directory(original_rom, roms_directory, output_directory)
