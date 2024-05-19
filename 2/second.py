from PIL import Image

img = Image.open("image_1.jpg") 
print('mode = ', img.mode)

R, G, B = img.split()

mask = Image.new("L", img.size, 128)
img2 = Image.merge("RGBA", (R, G, B, mask))
print('1. mode = ', img2.mode)
img2.show()


img3 = img.convert("RGBA")
print('2. mode = ', img3.mode)
img3.show()

# pil_im = Image.open('image_1.jpg').convert('L')


img4 = img.convert("P", None, Image.FLOYDSTEINBERG, Image.ADAPTIVE, 128)
print('3. mode = ', img4.mode)