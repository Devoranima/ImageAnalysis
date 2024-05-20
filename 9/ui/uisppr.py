from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QMainWindow, QComboBox, QLabel, QDialog
from db.dbController import getMaterials
from ui.uibd import DialogController

class MainWindowController(QMainWindow):
  def __init__(self):
    super(MainWindowController, self).__init__()
    uic.loadUi("ui/uisppr.ui", self)

    self.addBindings()
    self.addListeners()
    self.fetchMaterials()
    self.show()
  

  def addBindings(self):
    self.selectMaterialComboBox = self.findChild(QComboBox, "selectMaterialComboBox")
    self.ChangeMaterialsButton = self.findChild(QPushButton, "ChangeMaterialsButton")

    self.materialLabels = dict()
    self.materialLabels["PorosityValue"] = self.findChild(QLabel, "PorosityValue")
    self.materialLabels["PorosityDeviationValue"] = self.findChild(QLabel, "PorosityDeviationValue")
    self.materialLabels["SquareValue"] = self.findChild(QLabel, "SquareValue")
    self.materialLabels["SquareDeviationValue"] = self.findChild(QLabel, "SquareDeviationValue")

  def addListeners(self):
    self.selectMaterialComboBox.currentIndexChanged.connect(self.selectMaterialComboBox_currentIndexChangedListener)
    self.ChangeMaterialsButton.clicked.connect(self.openDialog)
  
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


