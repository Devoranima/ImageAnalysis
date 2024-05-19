from PIL import Image
from pylab import *

im = array(Image.open("image.jpg"))
imshow(im)
x = [100, 100, 400, 400]
y = [200, 500, 200, 500]

plot(x, y, "r*")
plot(x[:2], y[:2])

title('Plotting')
show()
axis('off')

imshow(im)
plot(x, y)
show()

imshow(im)
plot(x, y, 'go-')
show()

imshow(im)
plot(x, y, 'ks:')
show()
