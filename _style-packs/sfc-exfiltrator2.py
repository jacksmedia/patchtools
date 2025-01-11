from pathlib import Path
import shutil

# Define directories
style_packs_dir = Path(__file__).parent  # Current working directory
tools_dir = style_packs_dir.parent  # One directory up
patchwork_dir = tools_dir.parent  # Two directories up
modified_roms = patchwork_dir / "modified_roms2"

# Function to copy then delete local .sfc files
def move_sfc_files(src_dir, destination_dir):
    # Iterates over .sfc files in local directory
    for sfc_file in src_dir.glob("*.sfc"):
        try:
            # Copy file to destination
            shutil.copy2(sfc_file, destination_dir / sfc_file.name)
            print(f"Copied {sfc_file} to { destination_dir / sfc_file.name }")

            # Delete local file in src_dir
            sfc_file.unlink()
            print(f"Deleted: {sfc_file}")
        except Exception as e:
            print(f"Error processing file {sfc_file}: {e}")

# Move and delete all local .sfc files
move_sfc_files(style_packs_dir, modified_roms)