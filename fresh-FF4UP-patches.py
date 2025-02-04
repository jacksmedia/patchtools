import os
import ips

# Function to generate an IPS patch
def create_ips_patch(original_rom, current_build, output_patch):
    try:
        # Load original and modified ROMs
        with open(current_build, 'rb') as orig, open(original_rom, 'rb') as mod:
            # Generate the patch using the 'ips' library
            patch = ips.Patch.create(orig, mod)

        # Save the IPS patch
        with open(output_patch, 'wb') as patch_file:
            patch_file.write(bytes(patch))  # writes using bytes method

        print(f"Patch file '{output_patch}' created successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to loop through the directory and create patches for each .sfc file
def batch_patch_directory(current_build, roms_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Loop through all files in the roms_directory
    for filename in os.listdir(roms_directory):
        # if filename.endswith(".s**"):  # Only expecting .sfc & .smc files, so this is good enough for now
        original_rom = os.path.join(roms_directory, filename)
        
        # Define the output patch file path
        patch_name = os.path.splitext(filename)[0] + ".ips"  # Change .sfc to .ips
        output_patch = os.path.join(output_directory, patch_name)

        # Create the patch for each ROM
        create_ips_patch(original_rom, current_build, output_patch)
        print(f"Created patch {output_patch}!")

# Core inputs defined
current_build = 'latest-build.sfc'  # Path to the original ROM
roms_directory = './original-8-roms'  # Directory containing modified ROMs
output_directory = './output_patches'  # Directory to save the patch files

# Runs script
batch_patch_directory(current_build, roms_directory, output_directory)
