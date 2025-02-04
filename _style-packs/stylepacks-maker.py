import os
import shutil
import ips
import io
from pathlib import Path

# Define directories
style_packs_dir = Path(__file__).parent  # Current working directory
tools_dir = style_packs_dir.parent  # One directory up
patchwork_dir = tools_dir.parent  # Two directories up

# Locate original ROM
rom_to_patch = patchwork_dir / '_UP-rom.sfc'

# Function to apply a single IPS patch to working ROM copy
def apply_patch(rom_path, patch_path):
    try:
        with open(rom_path, 'rb') as rom_file:
            rom_data = rom_file.read()
        with open(patch_path, 'rb') as patch_file:
            patch = ips.Patch.load(patch_file)

        rom_file_like = io.BytesIO(rom_data)
        patched_file_like = io.BytesIO(rom_data)  # Start with the original data

        patch.apply(rom_file_like, patched_file_like)

        with open(rom_path, 'wb') as rom_file:
            rom_file.write(patched_file_like.getvalue())  # Get the patched data as bytes
        
        print(f"Patch '{patch_path}' applied successfully!")
    except Exception as e:
        print(f"An error occurred while applying '{patch_path}': {e}")

# Function to sequentially apply all patches in a directory to a working ROM copy & create a manifest of changes
def sequential_patch_rom(rom_file, patch_directory):
    try:
        # Create a working copy of ROM file
        rom_filename = f'{patch_directory.name}-Plus.sfc'
        working_rom = style_packs_dir / rom_filename
        shutil.copyfile(rom_file, working_rom)
        print(f"Created working copy of the ROM: {working_rom}")

        # List all .ips files in the patch directory, sorted alphanumerically
        # Critical for patches which need to get applied earlier ( "_" as first char in filename works well)
        patch_files = sorted(
            (f for f in os.listdir(patch_directory) if f.endswith('.ips')),
            key=lambda x: x.casefold()
        )
        if not patch_files: # baseline IPS undiscovery error
            print(f"No .ips files found in the directory: {patch_directory}")
            return

        # Create manifest file
        manifest_path = style_packs_dir / f'{patch_directory.name}-manifest.txt'
        with open(manifest_path, 'w') as manifest:
            for patch_file in patch_files:
                patch_path = patch_directory / patch_file
                manifest.write(f"{patch_file}\n")
                apply_patch(working_rom, patch_path)

        print(f"All patches applied successfully to {working_rom}!")
        print(f"Manifest created at {manifest_path}")

    except Exception as e:
        print(f"An error occurred in directory '{patch_directory}': {e}")

# Function to process all stylepack subdirectories
def process_all_directories(base_directory, rom_file):
    for subdirectory in base_directory.iterdir():
        if subdirectory.is_dir():
            print(f"Processing directory: {subdirectory}")
            sequential_patch_rom(rom_file, subdirectory)

# Example usage
process_all_directories(style_packs_dir, rom_to_patch)
