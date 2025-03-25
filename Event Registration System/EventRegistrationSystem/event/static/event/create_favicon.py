from PIL import Image, ImageDraw, ImageFont
import os

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create a new image with a white background
img = Image.new('RGB', (32, 32), color='white')
draw = ImageDraw.Draw(img)

# Draw a blue circle
draw.ellipse([2, 2, 30, 30], fill='#007bff')

try:
    # Try to use Arial font
    font = ImageFont.truetype('arial.ttf', 24)
except OSError:
    # Fallback to default font if Arial is not available
    font = ImageFont.load_default()

# Draw the letter 'E' in white
draw.text((8, 4), 'E', fill='white', font=font)

# Save as ICO in the same directory as this script
favicon_path = os.path.join(current_dir, 'favicon.ico')
img.save(favicon_path) 