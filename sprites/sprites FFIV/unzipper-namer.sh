#!/bin/bash

# Loop through all zip files in the current directory
for zip_file in *.zip; do
    # Extract the base name of the zip file (without extension)
    base_name="${zip_file%.zip}"
    
    # Create a directory with the base name
    mkdir -p "$base_name"
    
    # Extract the contents of the zip file into the newly created directory
    unzip -q "$zip_file" -d "$base_name"
    
    # Loop through all files with .s* extensions in the extracted folder
    for file in "$base_name"/*.s*; do
        # Check if the file exists (in case there are no .s* files)
        if [[ -f "$file" ]]; then
            # Extract the file extension
            extension="${file##*.}"
            
            # Rename the file to match the directory name with its extension
            new_name="${base_name}.${extension}"
            
            # Rename the file and move it to the parent directory
            mv "$file" "$new_name"
        fi
    done
done
