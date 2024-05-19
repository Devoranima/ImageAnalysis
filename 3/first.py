from PIL import Image


img = Image.open("image_1.jpg")
img.show() 
for x in range(img.size[0]):
 for y in range(img.size[1]):
  r,g,b = img.getpixel((x,y))
  img.putpixel((x,y),(b, r,g))
img.show() # замена каналов
