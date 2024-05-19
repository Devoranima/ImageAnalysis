from PIL import Image

img = Image.open("image_1.png") 
#img.show()
print('size = ', img.size)
print('format = ', img.format)
print('mode = ', img.mode)
print('border box = ', img.getbbox())
print(img.info)