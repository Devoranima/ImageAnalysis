from PIL import Image

img = Image.open("image.jpg")
img2 = img.crop([0, 0, 100, 100])
img2.load()
print("size = ", img2.size)



print("size = ", img.size)
img.show()

box = (100,100,300,300)#берем кусок изображения:

img3 = img.crop(box)
newsize = (400, 400)
img3nr = img3.resize(newsize)
img3nr.show() 