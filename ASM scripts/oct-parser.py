import re
import json

# Function to parse a line of the disassembly
def parse_line(line):
    # Regex patterns for parsing lines
    address_pattern = r'([A-F0-9]{2}/[A-F0-9]{4}):'
    opcode_pattern = r'([A-F0-9]{2} [A-F0-9]{2}(?: [A-F0-9]{2})*)'
    comment_pattern = r';\s*(.*)'

    # Match the patterns
    address_match = re.search(address_pattern, line)
    opcode_match = re.search(opcode_pattern, line)
    comment_match = re.search(comment_pattern, line)

    address = address_match.group(1) if address_match else None
    opcode = opcode_match.group(1) if opcode_match else None
    comment = comment_match.group(1) if comment_match else None

    return address, opcode, comment

# Function to parse the entire disassembly text
def parse_disassembly(disassembly_text):
    functions = []
    current_function = {"address": "", "instructions": [], "comments": []}
    lines = disassembly_text.splitlines()

    for line in lines:
        # Check for function start (denoted by ';' comments)
        if line.strip().startswith(";"):
            if current_function["address"]:
                functions.append(current_function)
                current_function = {"address": "", "instructions": [], "comments": []}
            current_function["comments"].append(line.strip()[2:])

        else:
            address, opcode, comment = parse_line(line)
            if address and opcode:
                if not current_function["address"]:
                    current_function["address"] = address

                current_function["instructions"].append({
                    "address": address,
                    "opcode": opcode,
                    "comment": comment
                })

    # Add the last function if present
    if current_function["address"]:
        functions.append(current_function)

    return functions

# Function to convert parsed data to JSON
def disassembly_to_json(disassembly_text):
    parsed_functions = parse_disassembly(disassembly_text)
    return json.dumps({"functions": parsed_functions}, indent=4)

# Function to read disassembly from a file and save JSON output to a file
def disassembly_file_to_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
        disassembly_text = file.read()
    
    json_output = disassembly_to_json(disassembly_text)
    
    with open(output_file, 'w', encoding='utf-8') as json_file:  # Ensure the output file is also in UTF-8
        json_file.write(json_output)


# Test the script with a file
input_file = 'Ff5j_asm.txt'  # Update this path
output_file = 'disassembly_test_output.json'      # Update this path
disassembly_file_to_json(input_file, output_file) # Uncomment this line to run with files
