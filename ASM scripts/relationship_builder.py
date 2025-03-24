import json
import re

def parse_relationships(input_json_file, output_json_file):
    with open(input_json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    function_data = data['functions']
    function_relationships = {}

    for func in function_data:
        address = func['address']
        instructions = func['instructions']
        related_functions = set()

        # Iterate through instructions to find references to other functions
        for instruction in instructions:
            opcode = instruction['opcode']
            comment = instruction['comment']
            
            # Check for jump or branch instructions that point to other addresses
            match = re.search(r'(4C|20|B2|6B|F0|D0|30|80) ([0-9A-F]{2}) ([0-9A-F]{2})', opcode)
            if match:
                target_address = f"{match.group(2)}/{match.group(3)}"
                # Add the function address to the related functions set
                related_functions.add(target_address)

            # Check the comment for any indications of relationships
            if comment:
                if 'get' in comment or 'branch' in comment:
                    # Example logic for linking based on comments (adjust as needed)
                    related_functions.add(comment)

        function_relationships[address] = list(related_functions)

    with open(output_json_file, 'w', encoding='utf-8') as file:
        json.dump(function_relationships, file, indent=4)

    print(f"Relationships parsed and saved to {output_json_file}")

# Run the script
parse_relationships('disassembly_test_output.json', 'function_relationships.json')
