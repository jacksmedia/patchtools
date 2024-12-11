from pathlib import Path
import shutil

# Define directories
style_packs_dir = Path(__file__).parent  # Current working directory
tools_dir = style_packs_dir.parent  # One directory up
patchwork_dir = tools_dir.parent  # Two directories up
documents_dir = patchwork_dir.parent # 3 dirs up, branch for other dirs
style_packs_archive = documents_dir / "romhacking\\FFIV hacks\\__Final Fantasy 4 Ultima Plus patch archive\\new style packs (change many things)"

# Function to copy then delete local .sfc files
def move_sfc_files(src_dir, destination_dir):
    # Iterates over .sfc files in local directory
    for txt_file in src_dir.glob("*-manifest.txt"):
        try:
            # Copy file to destination
            shutil.copy2(txt_file, destination_dir / txt_file.name)
            print(f"Copied {txt_file } to { destination_dir / txt_file.name }")

            # Delete local file in src_dir
            txt_file.unlink()
            print(f"Deleted: {txt_file}")
        except Exception as e:
            print(f"Error processing file { txt_file }: {e}")

# Move and delete all local .sfc files
move_sfc_files(style_packs_dir, style_packs_archive)