from PIL import Image

img = Image.open("image.jpg")
print("size = ", img.size)


img2 = img.rotate(90)# Поворот на 90 градусов
print("size = ", img2.size)


img3 = img.rotate(45, Image.NEAREST)
print("size = ", img3.size)

img4 = img.rotate(45, expand=True)
print("size = ", img4.size)



img5 = img.transpose(Image.FLIP_LEFT_RIGHT)
img5.show()

img6 = img.transpose(Image.FLIP_TOP_BOTTOM)
img6.show()

img7 = img.transpose(Image.ROTATE_90)
img7.show()

img8 = img.transpose(Image.ROTATE_180)
img8.show()