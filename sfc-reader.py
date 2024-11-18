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
    battle_sprites_start = int(info['battle_sprites_start'][1:], 16) # 16 bc hex number
    pal_start = int(info['pal_start'][1:], 16) # [1:] strips the $
    map_sprites_start = int(info['map_sprites_start'][1:], 16) # [1:] strips the $


    # Read tiles of sprite data
    # will use the line below for map sprites
    battle_sprite_data = read_bytes(rom_filename, battle_sprites_start, 2048) # 48 tiles of 32 bytes each

    # Read 32 bytes of palette data
    palette_data = read_bytes(rom_filename, pal_start, 32) # 16 colors of 2 bytes each

    # Read 1536 bytes of map sprite data
    map_sprite_data = read_bytes(rom_filename, map_sprites_start, 1536) # 48 tiles of 32 bytes each

    print(f"Character: {character}")
    print(f"  Sprite Data: {battle_sprite_data.hex()}")
    print(f"  Palette Data: {palette_data.hex()}")
    print(f"  Map Sprite Data: {map_sprite_data.hex()}")