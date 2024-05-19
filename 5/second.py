# Подключаем модуль:
from PIL import Image

img = Image.open("image.jpg")
img2 = img.resize((200, 150))
print("size = ", img2.size)
img.paste((255, 0, 0), (9, 9, 211, 161))
img.paste(img2, (10, 10))
img.show()

img = Image.open("image.jpg")
white = Image.new("RGB", (img.size[0], 100), (255, 255, 255))
mask = Image.new("L", (img.size[0], 100), 64)
img.paste(white, (0, 0), mask)
img.show()

pil_im = Image.open('image.jpg').convert('L') 
box = (100, 100, 400, 400)
region = pil_im.crop(box)
region = region.transpose(Image.ROTATE_180)
pil_im.paste(region, box)
pil_im.show()
