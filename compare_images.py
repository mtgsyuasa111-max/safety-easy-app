import os
from PIL import Image
import hashlib

def get_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# Compare images in MTShop row 3
img2_path = r"extracted_images/MTShop/B3_img2_178x133.png"
img25_path = r"extracted_images/MTShop/B3_img25_1477x1108.png"
img48_path = r"extracted_images/MTShop/E3_img48_394x378.png"

for name, p in [("img2", img2_path), ("img25", img25_path), ("img48", img48_path)]:
    if os.path.exists(p):
        print(f"{name}: path={p}, size={os.path.getsize(p)} bytes, hash={get_hash(p)}")
        im = Image.open(p)
        print(f"  Dimensions: {im.width}x{im.height}, Format: {im.format}")
    else:
        print(f"{name} does not exist!")
