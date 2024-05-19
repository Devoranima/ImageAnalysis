from PIL import Image

img = Image.open("image_1.png") 
print('mode = ', img.mode)


obj = img.load()
print(obj[25, 45])
obj[25, 45] = (255, 0, 0)
print(obj[25, 45])
img.show()


print (img.getpixel((25, 45)))
img.putpixel((25, 45), (0, 0, 255))
print(img.getpixel((25, 45)))

img.show()