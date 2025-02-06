import os
import shutil
import io
from pathlib import Path

def apply_ips_patch(rom_data, ips_data):
    """Applies an IPS patch to the ROM data and returns the patched ROM."""
    IPS_HEADER = b"PATCH"
    IPS_FOOTER = b"EOF"

    if not ips_data.startswith(IPS_HEADER):
        raise ValueError("Invalid IPS file: Incorrect header.")

    offset = 5  # Skip header
    rom_data = bytearray(rom_data)  # Convert ROM to mutable bytearray

    while offset < len(ips_data):
        if offset + 3 <= len(ips_data) and ips_data[offset:offset + 3] == IPS_FOOTER:
            return rom_data  # Successfully patched

        if offset + 3 > len(ips_data):
            raise ValueError("Invalid IPS file: Unexpected EOF while reading address.")
        
        address = int.from_bytes(ips_data[offset:offset + 3], "big")
        offset += 3

        if offset + 2 > len(ips_data):
            raise ValueError("Invalid IPS file: Unexpected EOF while reading size.")
        
        size = int.from_bytes(ips_data[offset:offset + 2], "big")
        offset += 2

        if size == 0:
            # RLE Encoding
            if offset + 3 > len(ips_data):
                raise ValueError("Invalid IPS file: Unexpected EOF in RLE section.")
            
            rle_size = int.from_bytes(ips_data[offset:offset + 2], "big")
            rle_byte = ips_data[offset + 2]
            offset += 3

            # Expand ROM if needed
            if address + rle_size > len(rom_data):
                rom_data.extend(b'\x00' * (address + rle_size - len(rom_data)))

            rom_data[address:address + rle_size] = bytes([rle_byte]) * rle_size
        else:
            # Normal patch
            if offset + size > len(ips_data):
                raise ValueError("Invalid IPS file: Unexpected EOF in patch data.")
            
            patch_data = ips_data[offset:offset + size]
            offset += size

            # Expand ROM if needed
            if address + size > len(rom_data):
                rom_data.extend(b'\x00' * (address + size - len(rom_data)))

            rom_data[address:address + size] = patch_data

    raise ValueError("Invalid IPS file: Missing EOF marker.")

def batch_patch_rom():
    """Applies all .ips patches in the /patches directory to _original-rom.sfc."""
    patches_dir = Path("./patches")
    output_dir = Path("./modified_roms")
    rom_path = Path("./_original-rom.sfc")

    if not rom_path.exists():
        print(f"Error: {rom_path} not found!")
        return

    output_dir.mkdir(exist_ok=True)

    for ips_file in patches_dir.glob("*.ips"):
        try:
            print(f"Patching with {ips_file.name}...")
            with ips_file.open("rb") as f:
                ips_data = f.read()
            
            with rom_path.open("rb") as f:
                rom_data = f.read()

            patched_rom = apply_ips_patch(rom_data, ips_data)
            output_rom_path = output_dir / ips_file.with_suffix(".sfc").name

            with output_rom_path.open("wb") as f:
                f.write(patched_rom)

            print(f"✔️ Patched ROM saved as: {output_rom_path}")

        except Exception as e:
            print(f"❌ Error patching {ips_file.name}: {e}")

if __name__ == "__main__":
    batch_patch_rom()
