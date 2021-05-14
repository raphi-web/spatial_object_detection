import os
from PIL import Image

img_files = [i for i in os.listdir() if i.split(".")[-1] == "tif"]

for img_file in img_files:
    img = Image.open(img_file).convert("RGB")
    img_name = img_file.split('.')[0]  + "_" + img_file.split('.')[1] 
    img.save(f"converted/{img_name}.jpg")