import json
from pathlib import Path

# Core Read function
def read_bytes(filename, offset, length):
    try:
        print(f"Attempting to read {length} bytes from {filename} starting at offset {hex(offset)}")
        with open(filename, 'rb') as f:
            f.seek(offset)
            data = f.read(length)
            print(f"Read successful: {len(data)} bytes captured")
            return data
    except Exception as e:
        print(f"Error reading bytes: {e}")
        return b''

# Mapping adjustment function
def hirom_to_lorom(offset):
    return (offset & 0x3FFFFF) | 0x8000

# Bulk processing function
def bulk_read_rom(original_rom, offsets, output_dir):
    print(f"Original rom file: {original_rom}")
    print(f"Output directory: {output_dir}")

    output_dir.mkdir(exist_ok=True) # Verify output_dir exists

    for entry, info in offsets.items():
        try:
            # Parse start and end offsets, assure HiROM addressing
            offset_start = hirom_to_lorom(int(info['offset_start'], 16))  # Hexadecimal conversion
            offset_end = hirom_to_lorom(int(info['offset_end'], 16))  # Hexadecimal conversion
            # offset_start = int(info['offset_start'], 16)  # Hexadecimal conversion
            # offset_end = int(info['offset_end'], 16)  # Hexadecimal conversion
            print(f"Adjusted Offset Start: {hex(offset_start)}, End: {hex(offset_end)}")

            # Calculate length dynamically
            length = offset_end - offset_start
            print(f"Processing entry: {entry}")
            print(f"Offset start: {hex(offset_start)}, Offset end: {hex(offset_end)}, Length: {length}")


            # Read specified range of bytes
            captured_bytes = read_bytes(original_rom, offset_start, length)

            # Save captured bytes as hexbytes to file with 'entry' as name
            if captured_bytes:
                output_file = output_dir / f"{entry.replace(' ','_')}.txt"
                with open(output_file, 'w') as f:
                    hex_string = captured_bytes.hex() # Convert bytes to hexbytes
                    hexbytes_string = ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2)) #Write in pairs
                    f.write(hexbytes_string)
                print(f"Captured hex bytes written to {output_file}")
            else:
                print(f"No data captured for entry: {entry}")

        except Exception as e:
            print(f"Error processing entry {entry}: {e}")

# Import offsets from JSON
try:
    with open('ffvj.json', 'r') as f:
        offsets = json.load(f)
    print("Offsets successfully loaded from JSON")
except Exception as e:
    print(f"Error loading offsets: {e}")
    offsets = {}

# Define directories
script_dir = Path(__file__).parent
output_dir = script_dir / "FFVJ-scraping-output"

# Set file paths
original_rom = script_dir.parent / "ffvj.sfc"

# Check if original ROM exists
if not original_rom.exists():
    print(f"Error: Original ROM file {original_rom} does not exist")
else:
    # Batch process invocation
    bulk_read_rom(original_rom, offsets, output_dir)
