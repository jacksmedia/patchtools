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

# Function to process a single ROM
def readfrom_rom(original_rom, offsets, output_file):
    print(f"Original ROM file: {original_rom}")
    print(f"Output file: {output_file}")
    
    for entry, info in offsets.items():
        try:
            # Debugging step for rom ID
            rom_size = original_rom.stat().st_size
            print(f"ROM file size: {rom_size} bytes")

            # Parse start and end offsets
            offset_start = int(info['offset_start'], 16)  # Hexadecimal conversion
            offset_end = int(info['offset_end'], 16)  # Hexadecimal conversion

            # Calculate length dynamically
            length = offset_end - offset_start
            print(f"Processing entry: {entry}")
            print(f"Offset start: {hex(offset_start)}, Offset end: {hex(offset_end)}, Length: {length}")

            # Read the specified range of bytes
            # captured_bytes = read_bytes(original_rom, offset_start, length)

            # Debug test values injection
            test_offset = 0xCA0000
            test_length = 16  # Read 16 bytes
            captured_bytes = read_bytes(original_rom, test_offset, test_length)
            print(f"Test read (16 bytes): {captured_bytes.hex()}")


            # Save captured bytes if any
            if captured_bytes:
                with open(output_file, 'wb') as f:
                    f.write(captured_bytes)
                print(f"Captured bytes written to {output_file}")
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

# Set file paths
original_rom = script_dir / 'ffvj.sfc'
output_file = script_dir / f"captured-bytes-{original_rom.stem}.txt"

# Check if original ROM exists
if not original_rom.exists():
    print(f"Error: Original ROM file {original_rom} does not exist")
else:
    # Batch process invocation
    readfrom_rom(original_rom, offsets, output_file)
