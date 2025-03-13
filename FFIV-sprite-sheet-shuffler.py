from PIL import Image

## This takes a PNG file of exactly 112 x 48 pixels
## and outputs an image of exactly 128 x 32 pixels;
## the arrangement of the 8 x 8 pixel tiles is optimized from
## the ff6tools layout (contiguous) to the rom-specific layout (jumbled).
## 
## Created on 12 Mar 2025 by xJ4cks & ChatGPT4


def rearrange_tiles(input_path, output_path):
    TILE_SIZE = 8
    INPUT_WIDTH, INPUT_HEIGHT = 112, 48
    OUTPUT_WIDTH, OUTPUT_HEIGHT = 128, 32
    
    # Define the hardcoded tile mapping from input to output grid
    tile_map = [
        1,  2, 15, 16, 29, 30,  3,  4, 17, 18, 31, 32, 33, 34,  7,  8,
       21, 22, 35, 36, 23, 37, 25, 26, 39, 40, 14, 28, 41, 42, 43, 44,
       57, 58, 71, 72, 45, 46, 59, 60, 73, 74, 61, 62, 63, 75, 76, 77,
       54, 55, 56, 68, 69, 70, 82, 83, 84, 50, 51, 64, 65, 78, 79, 66
    ]
    
    # Convert tile_map to zero-indexed
    tile_map = [t - 1 for t in tile_map]
    
    # Open input image
    img = Image.open(input_path)
    
    # Extract tiles from input image
    tiles = []
    for y in range(0, INPUT_HEIGHT, TILE_SIZE):
        for x in range(0, INPUT_WIDTH, TILE_SIZE):
            tile = img.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))
            tiles.append(tile)
    
    # Create output image
    output_img = Image.new("RGBA", (OUTPUT_WIDTH, OUTPUT_HEIGHT))
    
    # Place tiles in new arrangement
    for i, tile_index in enumerate(tile_map):
        x = (i % (OUTPUT_WIDTH // TILE_SIZE)) * TILE_SIZE
        y = (i // (OUTPUT_WIDTH // TILE_SIZE)) * TILE_SIZE
        output_img.paste(tiles[tile_index], (x, y))
    
    # Save output image
    output_img.save(output_path)
    print(f"Rearranged image saved as {output_path}")

# Example usage
rearrange_tiles("input.png", "output.png")
