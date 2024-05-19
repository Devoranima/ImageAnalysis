from PIL import Image

img = Image.open("image_1.jpg") 

img.save("tmp/tmp.jpg")
# в формате BMP:
img.save("tmp/tmp.bmp", "BMP")
f = open("tmp/tmp2.bmp", "wb")
# Передаем файловый объект
img.save(f, "BMP")
f.close()
