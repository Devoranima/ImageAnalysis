from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QMainWindow, QComboBox, QLabel, QAction, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSlider
from PyQt5.QtGui import QPixmap, QImage
from controllers.dbController import getMaterials
from controllers.dialogController import DialogController
from PIL import Image, ImageEnhance
import cv2
import numpy as np



def pil2pixmap(im):
  """Функция для перевода изображения из библиотеки pillow в pixelmap из библиотеки PyQt5 для последующего отображения в пользовательском интерфейсе

  Args:
      im (ndarray): Исходное изображание pillow

  Returns:
      pixmap: Изображение в виде набора пикселей
  """
  if im.mode == "RGB":
      r, g, b = im.split()
      im = Image.merge("RGB", (b, g, r))
  elif  im.mode == "RGBA":
      r, g, b, a = im.split()
      im = Image.merge("RGBA", (b, g, r, a))
  elif im.mode == "L":
      im = im.convert("RGBA")
  # Bild in RGBA konvertieren, falls nicht bereits passiert
  im2 = im.convert("RGBA")
  data = im2.tobytes("raw", "RGBA")
  qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
  pixmap = QPixmap.fromImage(qim)
  return pixmap

class MainWindowController(QMainWindow):
  def __init__(self):
    super(MainWindowController, self).__init__()
    uic.loadUi("ui/uisppr.ui", self)

    self.filename = None
    self.addBindings()
    self.addListeners()
    self.fetchMaterials()

  def addBindings(self):
    """Метод 'привязывает' элементы интерфейса к инстанции класса контроллера через метод findChild 
    """
    self.selectMaterialComboBox = self.findChild(QComboBox, "selectMaterialComboBox")
    self.ChangeMaterialsButton = self.findChild(QPushButton, "ChangeMaterialsButton")
    self.saveInReportBtn = self.findChild(QPushButton, "saveInReportBtn")

    self.materialLabels = dict()
    self.materialLabels["PorosityValue"] = self.findChild(QLabel, "PorosityValue")
    self.materialLabels["PorosityDeviationValue"] = self.findChild(QLabel, "PorosityDeviationValue")
    self.materialLabels["SquareValue"] = self.findChild(QLabel, "SquareValue")
    self.materialLabels["SquareDeviationValue"] = self.findChild(QLabel, "SquareDeviationValue")


    self.resultLabels = dict()
    self.resultLabels["PorosityResultValue"] = self.findChild(QLabel, "PorosityResultValue")
    self.resultLabels["PorosityVerdictResultValue"] = self.findChild(QLabel, "PorosityVerdictResultValue")
    self.resultLabels["BadCountorsAmountValue"] = self.findChild(QLabel, "BadCountorsAmountValue")

    self.SourceImageView = self.findChild(QGraphicsView, "SourceImageView")
    self.FilteredImageView = self.findChild(QGraphicsView, "FilteredImageView")
    self.ResultImageView = self.findChild(QGraphicsView, "ResultImageView")

    self.ImageContrastSlider = self.findChild(QSlider, "ImageContrastSlider")
    self.ImageBrightnessSlider = self.findChild(QSlider, "ImageBrightnessSlider")
    self.ImageSharpnessSlider = self.findChild(QSlider, "ImageSharpnessSlider")

    self.actionOpenFile = self.findChild(QAction, "actionOpen")


  def addListeners(self):
    """Метод добавляет слушатели событий к интерактивным элементам интерфейса
    """
    self.selectMaterialComboBox.currentIndexChanged.connect(self.selectMaterialComboBox_currentIndexChangedListener)
    self.ChangeMaterialsButton.clicked.connect(self.openDialog)
    self.actionOpenFile.triggered.connect(self.loadFile)

    self.ImageBrightnessSlider.valueChanged.connect(self.applyFilters)
    self.ImageContrastSlider.valueChanged.connect(self.applyFilters)
    self.ImageSharpnessSlider.valueChanged.connect(self.applyFilters)
    self.saveInReportBtn.clicked.connect(self.saveInReport)

  def loadFile(self): 
    """Метод загружает путь к изображению через модальное окно QFileDialog 
    """
    filename, _ = QFileDialog.getOpenFileName(
        self,
        "Select a File", 
        None, 
        "Images (*.png *.jpg)"
    )
    if filename:
      self.filename = filename
      self.loadImage()

  def loadImage(self):
    """Метод загружает изображение в окна оригинального и отфильтрованного изображения
    """
    self.loadSourceImage()
    self.loadFilteredImage()
  
  def saveInReport(self):
    """Метод вызывается при нажатии кнопки Сохранить в отчет. Вызывает метод explore для обработки изображения, а затем обновляет интерфейс пользователя

    Returns:
        None: При незагруженном изображении вернет None 
    """
    if self.filename == None: return None
    image, area_c, bad_contours_amount = self.explore()
    self.loadResultImage(image)
    self.resultLabels["PorosityResultValue"].setText(str(area_c))

    resultVerdict = "не в норме"
    color = 'red'
    if self.material[4] - self.material[5] < area_c < self.material[5] + self.material[4]:
      resultVerdict = "в норме"
      color = 'green'
    self.resultLabels["PorosityVerdictResultValue"].setText(resultVerdict)
    self.resultLabels["PorosityVerdictResultValue"].setStyleSheet("color: " + color)

    self.resultLabels["BadCountorsAmountValue"].setText(str(bad_contours_amount))

  def explore(self):
    """Метод обрабатывает отфильтрованное изображение, полученное через метод getFilteredImage и возвращает информацию по найденным порам

    Returns:
        image: Обработанное изображение с выделенными порами
        area_c: Пористость материала на изображении
        len(bad_contours): Количество пор, у которых площадь больше нормы
    """
    image = self.getFilteredImage()
    image = np.asarray(image)
    image = image[1:].copy()
    blured = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([120, 120, 120])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    good_contours = []
    bad_contours = []
    area_c = 0

    minArea = self.material[2] - self.material[3]
    maxArea = self.material[2] + self.material[3]
    for contour in contours:
      area_c += cv2.contourArea(contour)
      if minArea <= cv2.contourArea(contour) <= maxArea:
        good_contours.append(contour)
      else:
        bad_contours.append(contour)
    area_c = area_c / (image.shape[0] * image.shape[1])
    cv2.drawContours(image, good_contours, -1, (0, 255, 0), 3)
    cv2.drawContours(image, bad_contours, -1, (255, 0, 0), 3)

    return image, area_c, len(bad_contours)

  def loadResultImage(self, image):
    """Загружает обработанное изображение в пользователький интерфейс

    Args:
        image (ndarray): Обработанное изображение
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    ResultImageScene = QGraphicsScene()
    self.ResultImageView.setScene(ResultImageScene)
    pic = QGraphicsPixmapItem()
    pic.setPixmap(pil2pixmap(image))
    ResultImageScene.addItem(pic)

  def loadSourceImage(self):
    """Метод для загрузки исходного изображения в пользовательский интерфейс
    """
    sourceImageScene = QGraphicsScene()
    self.SourceImageView.setScene(sourceImageScene)

    pic = QGraphicsPixmapItem()
    image = QImage(self.filename)
    pic.setPixmap(QPixmap.fromImage(image))
    sourceImageScene.addItem(pic)

  def loadFilteredImage(self):
    """Метод для загрузки отфильтрованного изображения в пользовательский интерфейс
    """
    self.filteredImageScene = QGraphicsScene()
    self.FilteredImageView.setScene(self.filteredImageScene)
    self.applyFilters()

  def applyFilters(self):
    """Метод для применения фильтров для копии исходного изображения
    """
    self.filteredImageScene.clear()
    pic = QGraphicsPixmapItem()
    
    image = self.getFilteredImage()
    pic.setPixmap(pil2pixmap(image))
    self.filteredImageScene.addItem(pic)

  def getFilteredImage(self):
    """Метод для получения отфильтрованного изображения"""
    image = Image.open(self.filename)
 
    filter = ImageEnhance.Brightness(image)
    image = filter.enhance(self.ImageBrightnessSlider.value()/100)
    filter = ImageEnhance.Contrast(image)
    image = filter.enhance(self.ImageContrastSlider.value()/100+1)
    filter = ImageEnhance.Sharpness(image)
    image = filter.enhance(self.ImageSharpnessSlider.value()/100+1)

    return image

  def openDialog(self):
    """Метод для открытия диалогового окна выбора материала"""
    DialogController().exec_()
    self.fetchMaterials()

  def fetchMaterials(self):
    """Метод для получения списка материалов из базы данных"""
    self.materials = getMaterials()
    self.selectMaterialComboBox.clear()
    self.selectMaterialComboBox.addItems(x[1] for x in self.materials)

  def selectMaterialComboBox_currentIndexChangedListener(self):
    """Слушатель события изменения индекса в комбобоксе выбора материала"""
    self.material = self.materials[self.selectMaterialComboBox.currentIndex()]
    self.materialLabels["SquareValue"].setText(str(self.material[2]))
    self.materialLabels["SquareDeviationValue"].setText(str(self.material[3]))
    self.materialLabels["PorosityValue"].setText(str(self.material[4]))
    self.materialLabels["PorosityDeviationValue"].setText(str(self.material[5]))

