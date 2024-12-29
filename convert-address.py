import argparse

def hirom_to_pc(hirom_address):
    """
    Converts a HiROM address to a PC address;
    HiROM address must be in range 0xC00000 - 0xFFFFFF.
    """
    if hirom_address < 0xC00000 or hirom_address > 0xFFFFFF:
        raise ValueError("Invalid HiROM address: Must be between 0xC00000 and 0xFFFFFF.")
    
    pc_address = hirom_address - 0xC00000
    return f"${pc_address:06X}"  # Format as $HHHHHH

def main():
    parser = argparse.ArgumentParser(description="Convert HiROM address to PC-style address.")
    parser.add_argument("hirom_address", type=lambda x: int(x, 16), help="HiROM address (e.g., 0xCA0000).")
    
    args = parser.parse_args()
    
    try:
        pc_address = hirom_to_pc(args.hirom_address)
        print(f"PC-style address: {pc_address}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
