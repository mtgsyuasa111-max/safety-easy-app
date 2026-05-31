from PIL import Image
import numpy as np

img0_path = r"extracted_images/FirePump/B3_img0_138x184.png"
img11_path = r"extracted_images/FirePump/B3_img11_585x565.png"

im0 = Image.open(img0_path).convert('RGB')
im11 = Image.open(img11_path).convert('RGB')

im11_resized = im11.resize(im0.size)

arr0 = np.array(im0)
arr11 = np.array(im11_resized)
mse = np.mean((arr0 - arr11) ** 2)

print("MSE between img0 and resized img11 in FirePump B3:", mse)
if mse < 1000:
    print("They are the SAME image!")
else:
    print("They are DIFFERENT images!")
