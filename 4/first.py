# Подключаем модуль:
from PIL import Image
# Открываем файл:
img = Image.open("image.jpg")
# Создаем копию:
img2 = img.copy()
# Просматриваем копию:
img2.show() 


print("size = ", img2.size)
img2.thumbnail((400, 100), Image.LANCZOS)
print("size = ", img2.size)


newsize = (400, 400)
imgnr = img.resize(newsize)
imgnr.show()