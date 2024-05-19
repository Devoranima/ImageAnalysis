# Подключаем модуль:
from PIL import Image
# Открываем файл:
img = Image.open("image.jpg")

img.paste( (255, 0, 0), (0, 0, 100, 100) )
img.show()

img = Image.open("image.jpg")
img.paste( (0, 128, 0), img.getbbox() )
img.show()
