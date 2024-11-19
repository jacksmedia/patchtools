import json
from pathlib import Path # for subfolder
import shutil

# Core Read/Write functions
def read_bytes(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        data = f.read(length)
        return data

def write_bytes(filename, offset, data):
    with open(filename, 'rb+') as f:
        f.seek(offset)
        f.write(data)

# Function to process a single rom
def salvage_rom(original_rom, edited_rom, output_rom, offsets):
    # Create a fresh sfc for salvaged data
    shutil.copyfile(original_rom, output_rom)

    # Process each character's data
    for character, info in offsets.items():
        battle_sprites_start = int(info['battle_sprites_start'][1:], 16) # 16 bc hex number
        pal_start = int(info['pal_start'][1:], 16) # [1:] strips the $
        #map_sprites_start = int(info['map_sprites_start'][1:], 16)
        #map_pal_data = int(info['map_pal_index'][1:], 16)

        # Read & write 64 tiles of battle sprite data
        battle_sprite_data = read_bytes(edited_rom, battle_sprites_start, 2048) # 64 tiles of 32 bytes each
        write_bytes(output_rom, battle_sprites_start, battle_sprite_data) 

        # Read & write 32 bytes of battle palette data
        palette_data = read_bytes(edited_rom, pal_start, 32) # 16 colors of 2 bytes each
        write_bytes(output_rom, pal_start, palette_data)    

        # # Read 48 tiles of map sprite data
        # map_sprite_data = read_bytes(edited_rom, map_sprites_start, 1536) # 48 tiles of 32 bytes each

        # # Read 1 byte palette index
        # map_pal_data = read_bytes(edited_rom, map_pal_data, 1) # 1 byte index value

        # Read 16 tiles of portrait sprite data (256 bytes)
        # portrait_sprite_data = read_bytes(edited_rom, portrait_start, 256) 

        # Read 8 colors (16 bytes) of portrait palette data 
        # portrait_pal_data = read_bytes(edited_rom, portrait_pal, 16)

        # Console test prints
        print(f"Character: {character}")
        print(f"  Sprite Data: {battle_sprite_data.hex()}")
        print(f"  Palette Data: {palette_data.hex()}")
        # Just working on the 1st half for now
        #print(f"  Map Sprite Data: {map_sprite_data.hex()}")
        #print(f"  Map Palette: {map_pal_data.hex()}")
        #print(f"  Portrait Sprite Data: {portrait_sprite_data.hex()}")
        #print(f"  Portrait Palette: {portrait_pal_data.hex()}")
        

# Batch processing function
def process_all_roms(corrupt_roms_dir, original_rom, offsets):
    # Iterate thru all corrupted roms in directory
    for corrupt_rom in corrupt_roms_dir.glob("*.sfc"):
        output_rom = corrupt_roms_dir.parent / f"_salvaged_{corrupt_rom.name}"
        print(f"Processing '{corrupt_rom}' into '{output_rom}'")
        salvage_rom(original_rom, corrupt_rom, output_rom, offsets)
    print("Batch process completed! Now make some fresh patches!")


# Import offsets from JSON
with open('offset_data.json', 'r') as f:
    offsets = json.load(f)


# Define directories
script_dir = Path(__file__).parent # this dir
corrupt_roms_dir = script_dir / 'corrupted'

# Set original rom path
original_rom = script_dir.parent / '_original-rom.sfc'

# Batch process invocation
process_all_roms(corrupt_roms_dir, original_rom, offsets)