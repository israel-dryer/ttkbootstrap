"""Create a 64x64 button-xs.png from the 60x60 source."""

from PIL import Image
import os

# Load the original
src_path = "src/ttkbootstrap/assets/elements/button-xs.png"
dst_path = "src/ttkbootstrap/assets/elements/button-xs-64.png"

img = Image.open(src_path)
print(f"Original size: {img.size}")

# Resize to 64x64
img_64 = img.resize((64, 64), Image.Resampling.LANCZOS)
print(f"New size: {img_64.size}")

# Save
img_64.save(dst_path)
print(f"Saved to: {dst_path}")

# Also create backup and update original
backup_path = "src/ttkbootstrap/assets/elements/button-xs-60.png"
img.save(backup_path)
print(f"Backed up original to: {backup_path}")

# Overwrite original with 64x64 version
img_64.save(src_path)
print(f"Updated original to 64x64")