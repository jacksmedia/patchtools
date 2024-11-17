import json

def read_bytes(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        data = f.read(length)
        return data

# imports locations to read in the rom
with open('offset_data.json', 'r') as f:
    data = json.load(f)

rom_filename = '_original-rom.sfc'

for character, info in data.items():
    sprites_start = int(info['sprites_start'][1:], 16) # 16 bc hex number
    pal_start = int(info['pal_start'][1:], 16)

    # Read 16 bytes of sprite data
    sprite_data = read_bytes(rom_filename, sprites_start, 1536) # 48 tiles of 32 bytes each

    # Read 32 bytes of palette data
    palette_data = read_bytes(rom_filename, pal_start, 32) # 16 colors of 2 bytes each

    print(f"Character: {character}")
    print(f"  Sprite Data: {sprite_data.hex()}")
    print(f"  Palette Data: {palette_data.hex()}")