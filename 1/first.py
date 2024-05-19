from PIL import Image
import io

img = Image.open("image_1.png") 
img.show()

img = Image.open("image_2.png")
img = img.convert("L")
img.show()  


f = open("image_3.png", "rb")
img = Image.open(f)
img.show()
f.close()


f = open("image_4.png", "rb").read()
img = Image.open(io. BytesIO(f))
img = img.convert("L")
img.show()