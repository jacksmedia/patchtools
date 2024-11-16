from pathlib import Path
import shutil

# Define directories
style_packs_dir = Path(__file__).parent # bc current wd is /style-packs
patchwork_dir = style_packs_dir.parent # one dir up from this one
modified_roms_dir = patchwork_dir / 'modified_roms' # the sibling dir to this one

# Verify destination dir still exists
modified_roms_dir.mkdir(exist_ok=True)

# Scope the file types to copy
file_patterns = ("*.txt","*.sfc")

# Bulk copy files from here to destination dir
for pattern in file_patterns:
    for file in style_packs_dir.glob(pattern):
        if file.is_file(): # ignores dirs, only works on files
            destination = modified_roms_dir / file.name
            shutil.copy(file, destination) # copies file
            print(f'Copied {file.name} to {modified_roms_dir}')