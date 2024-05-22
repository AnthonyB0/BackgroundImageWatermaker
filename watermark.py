from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import io  # Import the io module
import os
# Function to remove the background using rembg
def remove_background(image_path):
    with open(image_path, 'rb') as i:
        input_image = i.read()
    output_image = remove(input_image)
    image = Image.open(io.BytesIO(output_image)).convert("RGBA")
    return image

# Function to add a white background
def add_white_background(image):
    white_bg = Image.new('RGBA', image.size, (255, 255, 255, 255))
    white_bg.paste(image, (0, 0), image)
    return white_bg

# Function to add a watermark behind the bottle
def add_watermark_behind(image, watermark_image_path):
    watermark = Image.open(watermark_image_path).convert("RGBA")
    
    # Resize watermark to match the size of the image
    watermark = watermark.resize(image.size, Image.LANCZOS)
    
    # Create a new image with white background
    combined = Image.new('RGBA', image.size, (255, 255, 255, 255))
    
    # Paste the watermark on the white background
    combined.paste(watermark, (0, 0), watermark)
    
    # Paste the original image on top of the watermark
    combined.paste(image, (0, 0), image)
    
    return combined.convert('RGB')

# Directory with images
input_dir = 's/'  # Update to the correct path if needed
output_dir = 'out/'  # Update to the correct path if needed
watermark_image = 'watermark.png'  # Path to your watermark image


# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each image
for filename in os.listdir(input_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        
        # Remove background
        foreground = remove_background(input_path)
        
        # Add watermark behind the image with a white background
        img_with_watermark = add_watermark_behind(foreground, watermark_image)
        
        # Save output
        output_path = os.path.join(output_dir, filename)
        img_with_watermark.save(output_path)
        print(f"Saved: {output_path}")

print("Processing complete.")