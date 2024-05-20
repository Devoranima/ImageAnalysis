from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QMainWindow, QComboBox, QLabel, QAction, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSlider
from PyQt5.QtGui import QPixmap, QImage
from db.dbController import getMaterials
from ui.uibd import DialogController
from PIL import Image, ImageEnhance
import PIL.ImageQt as PQ

def pil2pixmap(im):
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
    self.selectMaterialComboBox = self.findChild(QComboBox, "selectMaterialComboBox")
    self.ChangeMaterialsButton = self.findChild(QPushButton, "ChangeMaterialsButton")

    self.materialLabels = dict()
    self.materialLabels["PorosityValue"] = self.findChild(QLabel, "PorosityValue")
    self.materialLabels["PorosityDeviationValue"] = self.findChild(QLabel, "PorosityDeviationValue")
    self.materialLabels["SquareValue"] = self.findChild(QLabel, "SquareValue")
    self.materialLabels["SquareDeviationValue"] = self.findChild(QLabel, "SquareDeviationValue")

    self.SourceImageView = self.findChild(QGraphicsView, "SourceImageView")
    self.FilteredImageView = self.findChild(QGraphicsView, "FilteredImageView")

    self.ImageContrastSlider = self.findChild(QSlider, "ImageContrastSlider")
    self.ImageBrightnessSlider = self.findChild(QSlider, "ImageBrightnessSlider")
    self.ImageSharpnessSlider = self.findChild(QSlider, "ImageSharpnessSlider")

    self.actionOpenFile = self.findChild(QAction, "actionOpen")

  def addListeners(self):
    self.selectMaterialComboBox.currentIndexChanged.connect(self.selectMaterialComboBox_currentIndexChangedListener)
    self.ChangeMaterialsButton.clicked.connect(self.openDialog)
    self.actionOpenFile.triggered.connect(self.loadFile)

    self.ImageBrightnessSlider.valueChanged.connect(self.applyFilters)
  
  def loadFile(self): 
    filename, ok = QFileDialog.getOpenFileName(
        self,
        "Select a File", 
        None, 
        "Images (*.png *.jpg)"
    )
    if filename:
      self.filename = filename
      self.loadImage()

  def loadImage(self):
    self.loadSourceImage()
    self.loadFilteredImage()

  def loadSourceImage(self):
    sourceImageScene = QGraphicsScene()
    self.SourceImageView.setScene(sourceImageScene)

    pic = QGraphicsPixmapItem()
    image = QImage(self.filename)
    pic.setPixmap(QPixmap.fromImage(image))
    sourceImageScene.addItem(pic)

  def loadFilteredImage(self):
    self.filteredImageScene = QGraphicsScene()
    self.FilteredImageView.setScene(self.filteredImageScene)

    pic = QGraphicsPixmapItem()
    image = Image.open(self.filename)
 
    filter = ImageEnhance.Brightness(image)
    image = filter.enhance(self.ImageBrightnessSlider.value()/100)
 
    pic.setPixmap(pil2pixmap(image))
    self.filteredImageScene.addItem(pic)

  def applyFilters(self):
    self.filteredImageScene.clear()
    pic = QGraphicsPixmapItem()
    image = Image.open(self.filename)
 
    filter = ImageEnhance.Brightness(image)
    image = filter.enhance(self.ImageBrightnessSlider.value()/100)
 
    pic.setPixmap(pil2pixmap(image))
    self.filteredImageScene.addItem(pic)

  def openDialog(self):
    DialogController().exec_()
    self.fetchMaterials()

  def fetchMaterials(self):
    self.materials = getMaterials()
    self.selectMaterialComboBox.clear()
    self.selectMaterialComboBox.addItems(x[1] for x in self.materials)

  def selectMaterialComboBox_currentIndexChangedListener(self):
    self.material = self.materials[self.selectMaterialComboBox.currentIndex()]
    self.materialLabels["SquareValue"].setText(str(self.material[2]))
    self.materialLabels["SquareDeviationValue"].setText(str(self.material[3]))
    self.materialLabels["PorosityValue"].setText(str(self.material[4]))
    self.materialLabels["PorosityDeviationValue"].setText(str(self.material[5]))

