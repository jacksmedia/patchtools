import json
from pathlib import Path

# Core Read function
def read_bytes(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        data = f.read(length)
        return data

# Function to process a single rom
def readfrom_rom(original_rom, offsets, output_file):
    for entry, info in offsets.items():
        # Parse start and end offsets
        offset_start = int(info['offset_start'], 16) # 16 bc hex number
        offset_end = int(info['offset_end'], 16) # 16 bc hex number

        # Compute length dynamically
        length = offset_end - offset_start

        # Read bytes indicated by offsets' range
        captured_bytes = read_bytes(original_rom, offset_start, length)
        
        # Write bytes to new file 
        with open(output_file, 'wb') as f:
            f.write(captured_bytes) 

        # Console test prints
        print(f"Entry: {entry}")
        print(f"Start: {hex(offset_start)}, End: {hex(offset_end)}")
        print(f"Captured bytes: {captured_bytes.hex()}")


# Import offsets from JSON
with open('ffvj.json', 'r') as f:
    offsets = json.load(f)


# Define directories
script_dir = Path(__file__).parent # this dir

# Set file paths
original_rom = script_dir / 'ffvj.sfc'
output_file = script_dir / f"captured-bytes-{original_rom.name}.txt"


# Function call
readfrom_rom(original_rom, offsets, output_file)