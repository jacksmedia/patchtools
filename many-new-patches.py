import sys
import os
from pathlib import Path
import ips

def create_patch(template_rom, target_rom, output_patch):
    try:
        # Load template and target ROMs
        with open(template_rom, 'rb') as template_file, open(target_rom, 'rb') as target_file:
            template_data = template_file.read()
            target_data = target_file.read()

        # Generate the IPS patch
        patch = ips.Patch.create(template_data, target_data)

        # Save the patch file
        with open(output_patch, 'wb') as patch_file:
            patch_file.write(bytes(patch))
        
        print(f"Patch created: {output_patch}")
    except Exception as e:
        print(f"Error creating patch for {target_rom}: {e}")

def main():
    # Ensure a template ROM filename was provided
    if len(sys.argv) != 2:
        print("Usage: python patch_maker.py <template_rom.sfc>")
        return

    template_rom_name = sys.argv[1]
    current_dir = Path(__file__).parent
    template_rom = current_dir / template_rom_name

    # Ensure the template ROM exists
    if not template_rom.exists():
        print(f"Error: Template ROM '{template_rom}' not found.")
        return

    # Iterate over all .sfc files in the current directory
    for rom_file in current_dir.glob("*.sfc"):
        # Skip the template ROM itself
        if rom_file.name == template_rom_name:
            continue

        # Define the output patch filename
        output_patch = rom_file.with_suffix(".ips")

        # Create the IPS patch
        create_patch(template_rom, rom_file, output_patch)

if __name__ == "__main__":
    main()
