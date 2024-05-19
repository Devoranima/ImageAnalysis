from PIL import Image
import matplotlib.pyplot as plt

img = Image.open("image.jpg")


plt.figure()
plt.hist(img.histogram(), 128)
plt.show()