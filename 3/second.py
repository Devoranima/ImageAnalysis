from PIL import Image


img = Image.open("image_1.jpg")
R, G, B = img.split()

img2 = Image.merge("RGB", (R, G, B))
print("mode = ", img2.mode)
img2.show()