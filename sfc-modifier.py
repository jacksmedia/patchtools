import json
# import os # will be used for entire dir iteration
import shutil

# Core Read Write functions
def read_bytes(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        data = f.read(length)
        return data

def write_bytes(filename, offset, data):
    with open(filename, 'rb+') as f:
        f.seek(offset)
        f.write(data)


# Import locations to read in the rom
with open('offset_data.json', 'r') as f:
    data = json.load(f)

# Load & create working roms
original_rom = '_original-rom.sfc'
edited_rom = 'edited-rom.sfc'
output_rom = f'__salvaged-{edited_rom}'

# Create a fresh sfc to receive exported edits
shutil.copyfile(original_rom, output_rom)

for character, info in data.items():
    battle_sprites_start = int(info['battle_sprites_start'][1:], 16) # 16 bc hex number
    pal_start = int(info['pal_start'][1:], 16) # [1:] strips the $
    map_sprites_start = int(info['map_sprites_start'][1:], 16)
    map_pal_data = int(info['map_pal_index'][1:], 16)

    # Read 64 tiles of sprite data
    battle_sprite_data = read_bytes(edited_rom, battle_sprites_start, 2048) # 48 tiles of 32 bytes each
    # Write tiles of sprite data
    write_bytes(output_rom, battle_sprites_start, battle_sprite_data) 

    # Read 32 bytes of palette data
    palette_data = read_bytes(edited_rom, pal_start, 32) # 16 colors of 2 bytes each
    # Write battle palette data
    write_bytes(output_rom, pal_start, palette_data)    

    # # Read 48 tiles of map sprite data
    # map_sprite_data = read_bytes(edited_rom, map_sprites_start, 1536) # 48 tiles of 32 bytes each

    # # Read 1 byte palette index
    # map_pal_data = read_bytes(edited_rom, map_pal_data, 1) # 1 byte index value


    # Console test prints
    print(f"Character: {character}")
    print(f"  Sprite Data: {battle_sprite_data.hex()}")
    print(f"  Palette Data: {palette_data.hex()}")
    # Just working on the 1st half for now
    #print(f"  Map Sprite Data: {map_sprite_data.hex()}")
    #print(f"  Map Palette: {map_pal_data.hex()}")