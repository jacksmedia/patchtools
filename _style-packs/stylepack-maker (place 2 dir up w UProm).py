from pathlib import Path
import os
import ips


# Define directories
pactchwork_dir = Path(__file__).parent # current working dir
documents_dir = pactchwork_dir.parent # 1 dir up

# Guarantee path is relative to this dir
script_dir = Path(__file__).parent
roms_directory = script_dir / "modified_roms"


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

# Running config
original_rom = './_UP-rom.sfc'  # Path to the original ROM (FF4 UP)
style_packs_archive = "C:\Users\J4cks\Desktop\work4\_ultima-project\__Final Fantasy 4 Ultima Plus patch archive\\new style packs (change many things)" # project style packs dir
output_directory = style_packs_archive  # Directory to save the patch files

batch_patch_directory(original_rom, roms_directory, output_directory)
