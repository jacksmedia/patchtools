import json
import re

def parse_relationships(json_file, output_file):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        disassembly_data = json.load(f)
    
    # Access the "functions" list directly
    functions_data = disassembly_data.get('functions', [])

    # Dictionary to hold relationships and addresses to functions
    function_relationships = {}
    address_to_function_map = {}

    # Expanded regex patterns for various branching and subroutine instructions
    jump_pattern = re.compile(r"JMP\s+\$([0-9A-F]{4})", re.IGNORECASE)
    subroutine_pattern = re.compile(r"JSR\s+\$([0-9A-F]{4})", re.IGNORECASE)
    branch_pattern = re.compile(r"(BEQ|BNE|BCC|BCS|BPL|BMI|BRA)\s+\$([0-9A-F]{4})", re.IGNORECASE)
    return_pattern = re.compile(r"(RTS|RTL)", re.IGNORECASE)

    # First Pass: Collect all addresses and map them to functions
    for func in functions_data:
        func_address = func.get('address')
        details = func

        # Initialize an entry in the function_relationships for this function
        function_relationships[func_address] = {
            "related_functions": [],
            "comments": []
        }

        # Map the address to the function for reference in the second pass
        address_to_function_map[func_address] = func

        # Debug: print each function address
        print(f"Collected function at address: {func_address}")

    # Second Pass: Populate relationships based on the collected data
    for func in functions_data:
        func_address = func.get('address')
        details = func
        related_functions = []
        comments = []

        # Debug: print each function address
        print(f"Processing function at address: {func_address}")

        # Ensure details is a dictionary and has 'instructions' before proceeding
        if isinstance(details, dict) and 'instructions' in details:
            for instruction in details['instructions']:
                if isinstance(instruction, dict) and 'code' in instruction:
                    # Debug: Print the instruction code
                    print(f"Instruction: {instruction['code']}")

                    # Match jump instructions
                    jump_match = jump_pattern.search(instruction['code'])
                    if jump_match:
                        target_address = jump_match.group(1)
                        if target_address in address_to_function_map:
                            related_functions.append({"type": "JMP", "address": target_address})
                            print(f"Found JMP to {target_address}")
                            comments.append(f"JMP to {target_address}")

                    # Match subroutine calls
                    subroutine_match = subroutine_pattern.search(instruction['code'])
                    if subroutine_match:
                        target_address = subroutine_match.group(1)
                        if target_address in address_to_function_map:
                            related_functions.append({"type": "JSR", "address": target_address})
                            print(f"Found JSR to {target_address}")
                            comments.append(f"JSR to {target_address}")

                    # Match branch instructions
                    branch_match = branch_pattern.search(instruction['code'])
                    if branch_match:
                        branch_type = branch_match.group(1)
                        target_address = branch_match.group(2)
                        if target_address in address_to_function_map:
                            related_functions.append({"type": branch_type, "address": target_address})
                            print(f"Found branch ({branch_type}) to {target_address}")
                            comments.append(f"Branch ({branch_type}) to {target_address}")

                    # Match return instructions (indicating end of a function)
                    return_match = return_pattern.search(instruction['code'])
                    if return_match:
                        print(f"Found return instruction ({return_match.group(1)}) at {func_address}")
                        comments.append(f"Return instruction ({return_match.group(1)})")

            # Store the relationships and comments for the function
            function_relationships[func_address] = {
                "related_functions": related_functions,
                "comments": comments
            }
        else:
            print(f"Warning: Function at address {func_address} has unexpected structure.")

    # Save the function relationships and comments to a new JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(function_relationships, f, indent=4)

    print(f"Relationships parsed and saved to {output_file}")

# Call the function with the input and output files
parse_relationships('disassembly_test_output.json', 'function_relationships1.json')
