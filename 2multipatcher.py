import os
import shutil
import ips
import io
from pathlib import Path

# Define directories
style_packs_dir = Path(__file__).parent # bc current wd is /style-packs
patchwork_dir = style_packs_dir.parent # one dir up from this one
# Locate RC rom
rom_to_patch = patchwork_dir / '_RC-rom.sfc'

# Function to apply a single IPS patch to the working ROM copy
def apply_patch(rom_path, patch_path):
    try:
        # Load the ROM and patch
        with open(rom_path, 'rb') as rom_file:
            rom_data = rom_file.read()
        with open(patch_path, 'rb') as patch_file:
            patch = ips.Patch.load(patch_file)

        # Create file-like objects for the original and patched ROM data
        rom_file_like = io.BytesIO(rom_data)
        patched_file_like = io.BytesIO(rom_data)  # Start with the original data

        # Apply the patch
        patch.apply(rom_file_like, patched_file_like)

        # Write the patched data back to the working ROM copy
        with open(rom_path, 'wb') as rom_file:
            rom_file.write(patched_file_like.getvalue())  # Get the patched data as bytes
        
        print(f"Patch '{patch_path}' applied successfully!")
    
    except Exception as e:
        print(f"An error occurred while applying '{patch_path}': {e}")

# Function to sequentially apply all IPS patches in a directory to a working ROM copy and create a manifest
def sequential_patch_rom(rom_file, patch_directory, working_directory):
    try:
        # Create a working copy of the ROM file
        rom_filename = os.path.basename(f'{patch_directory}.sfc')
        working_rom = os.path.join(working_directory, rom_filename)
        shutil.copyfile(rom_file, working_rom)
        print(f"Created working copy of the ROM: {working_rom}")

        # List all .ips files in the patch directory, sorted alphanumerically
        patch_files = sorted(f for f in os.listdir(patch_directory) if f.endswith('.ips'))
        
        if not patch_files:
            print("No .ips files found in the directory.")
            return
        
        # Create a manifest file in the working directory
        manifest_path = os.path.join(working_directory, f'{patch_directory}-manifest.txt')
        with open(manifest_path, 'w') as manifest:
            # Apply each patch sequentially to the working ROM
            for patch_file in patch_files:  # sorted alphanumerically
                patch_path = os.path.join(patch_directory, patch_file)
                
                # Log the patch name in the manifest
                manifest.write(f"{patch_file}\n")
                
                # Apply the patch to the working ROM
                apply_patch(working_rom, patch_path)

        print(f"All patches applied successfully to {working_rom}!")
        print(f"Manifest created at {manifest_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
rom_file = rom_to_patch  # Target ROM path (.sfc or .smc)
patch_directory = './2-Mercury'  # Directory containing .ips patches
patch_name = patch_directory.rstrip('./')
working_directory = './'  # Directory to store the working copy of the ROM and manifest

# Ensure the working directory exists
os.makedirs(working_directory, exist_ok=True)

sequential_patch_rom(rom_file, patch_directory, working_directory)
