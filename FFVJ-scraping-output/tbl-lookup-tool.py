import re
from pathlib import Path

# Function to parse .TBL file into a dictionary
def parse_tbl(tbl_file):
    translation_map = {}
    try:
        with open(tbl_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    translation_map[key.strip()] = value.strip()
                elif line.startswith("*") or line.startswith("/"):
                    # Handle special cases if needed
                    translation_map[line[1:].strip()] = f"[{line[0]}Logic]"
        print(f"TBL file '{tbl_file}' loaded successfully.")
    except Exception as e:
        print(f"Error reading TBL file: {e}")
    return translation_map

# Function to translate hex bytes using the TBL map
def translate_hex_file(hex_file, tbl_map, output_file):
    try:
        with open(hex_file, 'r', encoding='utf-8') as f:
            hex_data = f.read().replace(" ", "").strip()  # Remove spaces and clean up
        print(f"Hex file '{hex_file}' loaded. Length: {len(hex_data)} bytes.")

        # Translate hex bytes
        translated_text = []
        i = 0
        while i < len(hex_data):
            # Determine if 2-byte leading value
            if hex_data[i:i+2].upper() in {"17", "1E", "1F"} and i + 4 <= len(hex_data):
                two_byte_key = hex_data[i:1+4].upper() # Reads pair of bytes
                if two_byte_key in tbl_map:
                    translated_text.append(tbl_map[two_byte_key])
                    i += 4 # increment pointer
            
            # Return to 1-byte lookup
            byte = hex_data[i:i+2].upper()  # Read 2 characters at a time (1 byte)
            if byte in tbl_map:
                translated_text.append(tbl_map[byte])
            else:
                translated_text.append(f"[{byte}]")  # Placeholder for unmapped bytes
            i += 2

        # Write the translated text to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("".join(translated_text))
        print(f"Translated text written to '{output_file}'.")
    except Exception as e:
        print(f"Error processing hex file: {e}")

# Main script function
def main():
    # Define file paths
    script_dir = Path(__file__).parent
    tbl_file = script_dir / "dialogue-font.tbl"  # Replace with your TBL file
    hex_file = script_dir / "Dialogue-(J).txt"  # Replace with your hex file
    output_file = script_dir / "translated-Dialogue.txt"

    # Parse the TBL file
    tbl_map = parse_tbl(tbl_file)

    # Translate the hex file
    translate_hex_file(hex_file, tbl_map, output_file)

# Run the script
if __name__ == "__main__":
    main()
