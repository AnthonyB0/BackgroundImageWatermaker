from rembg import remove
from PIL import Image, ImageDraw
import io
import os

class WatermarkProcessor:
    def __init__(self, watermark_image_path):
        self.watermark_image_path = watermark_image_path
        self.watermark = Image.open(watermark_image_path).convert("RGBA")

    def remove_background(self, image_path):
        with open(image_path, 'rb') as i:
            input_image = i.read()
        output_image = remove(input_image)
        image = Image.open(io.BytesIO(output_image)).convert("RGBA")
        return image

    def add_white_background(self, image):
        white_bg = Image.new('RGBA', image.size, (255, 255, 255, 255))
        white_bg.paste(image, (0, 0), image)
        return white_bg


    def add_watermark_front(self, image):
        # Resize watermark to match the size of the image
        watermark = self.watermark.resize(image.size, Image.LANCZOS)

        # Create a new image with white background
        combined = Image.new('RGBA', image.size, (255, 255, 255, 255))

        # Paste the original image on the white background
        combined.paste(image, (0, 0), image)

        # Paste the watermark on top of the original image
        combined.paste(watermark, (0, 0), watermark)

        return combined.convert('RGB')
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
output_dir_behind = 'out/'  # Update to the correct path if needed
output_dir_front = 'out2/'  # Update to the correct path if needed
watermark_image = 'watermark3.png'  # Path to your watermark image

# Create output directories if they don't exist
if not os.path.exists(output_dir_behind):
    os.makedirs(output_dir_behind)

if not os.path.exists(output_dir_front):
    os.makedirs(output_dir_front)

# Create an instance of WatermarkProcessor
processor = WatermarkProcessor(watermark_image)

# Process each image
for filename in os.listdir(input_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        
        # Remove background
        foreground = processor.remove_background(input_path)
        
        # Add white background
        img_with_bg = processor.add_white_background(foreground)
        
        # Add watermark behind the image
        img_with_watermark_behind = add_watermark_behind(foreground, watermark_image)
        # Save output with watermark behind
        output_path_behind = os.path.join(output_dir_behind, filename)
        img_with_watermark_behind.save(output_path_behind)
        print(f"Saved with watermark behind: {output_path_behind}")
        
        # Add watermark in front of the image
        img_with_watermark_front = processor.add_watermark_front(img_with_bg)
        
        # Save output with watermark in front
        output_path_front = os.path.join(output_dir_front, filename)
        img_with_watermark_front.save(output_path_front)
        print(f"Saved with watermark in front: {output_path_front}")

print("Processing complete.")
