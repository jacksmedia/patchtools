import json

# for use with a file called ./bytes.json 
# prints object data to console
with open('bytes.json', 'r') as f:
    data = json.load(f)

for character, info in data.items():
    print(f"Character: {character}")
    print(f"  Sprites Start: {info['sprites_start']}")
    print(f"  Palette Start: {info['pal_start']}")
    print(f"  Palette: {info['palette']}")