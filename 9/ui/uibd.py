from PyQt5 import uic
from PyQt5.QtWidgets import  QPushButton, QWidget, QDialog, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
from db.dbController import getMaterials, deleteMaterial, addMaterial
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
  def __init__(self, data):
    super(TableModel, self).__init__()
    self._data = data

  def data(self, index, role):
    if role == Qt.DisplayRole:
      return self._data[index.row()][index.column()]

  def rowCount(self, index):
    return len(self._data)

  def columnCount(self, index):
    return len(self._data[0])
    
class DialogController(QDialog):
  def __init__(self):
    super(DialogController, self).__init__()
    uic.loadUi("ui/uibd.ui", self)
    self.addBindings()
    self.addListeners()
    self.fetchMaterials()

  def addBindings(self):
    self.MaterialsTableWidget = self.findChild(QTableWidget, "MaterialsTableview")
    labels = ['ID', 'Наименование', 'Площадь поры', 'Откл. от площади', 'Пористость', 'Откл. от пористости']
    self.MaterialsTableWidget.setHorizontalHeaderLabels(labels)

    self.DeleteMaterialID = self.findChild(QLineEdit, "DeleteMaterialID")
    self.DeleteMaterialBtn = self.findChild(QPushButton, "DeleteMaterialBtn")


    self.AddMaterialName = self.findChild(QLineEdit, "AddMaterialName")
    self.AddMaterialSquare = self.findChild(QLineEdit, "AddMaterialSquare")
    self.AddMaterialSquareDeviation = self.findChild(QLineEdit, "AddMaterialSquareDeviation")
    self.AddMaterialPorosity = self.findChild(QLineEdit, "AddMaterialPorosity")
    self.AddMaterialPorosityDeviation = self.findChild(QLineEdit, "AddMaterialPorosityDeviation")
    self.AddMaterialBtn = self.findChild(QPushButton, "AddMaterialBtn")


  def addListeners(self):
    self.DeleteMaterialBtn.clicked.connect(self.DeleteMaterialBtn_clicked)
    self.AddMaterialBtn.clicked.connect(self.AddMaterialBtn_clicked)
  
  def DeleteMaterialBtn_clicked(self):
    id = self.DeleteMaterialID.text()
    self.DeleteMaterialID.setText("")

    material = None
    for x in self.materials:
      if str(x[0]) == id:
        material = x
        break
    if material == None: 
      QMessageBox.warning(self, "Ошибка", "Такого ID не существует")
      return False

    deleteMaterial(id)
    self.fetchMaterials()
    QMessageBox.information(self, "Успешно", "Материал удален")

    return True
  
  def AddMaterialBtn_clicked(self):
    name = self.AddMaterialName.text()
    square = self.AddMaterialSquare.text()
    squareDeviation = self.AddMaterialSquareDeviation.text()
    porosity = self.AddMaterialPorosity.text()
    porosityDeviation = self.AddMaterialPorosityDeviation.text()
    if (name == "") or (square == "") or (squareDeviation == "") or (porosity == "") or (porosityDeviation == ""): return False

    addMaterial(name, square, squareDeviation, porosity, porosityDeviation)
    self.fetchMaterials()

    self.AddMaterialName.setText("")
    self.AddMaterialSquare.setText("")
    self.AddMaterialSquareDeviation.setText("")
    self.AddMaterialPorosity.setText("")
    self.AddMaterialPorosityDeviation.setText("")
    QMessageBox.information(self, "Успешно", "Материал добавлен")
    return True

  def fetchMaterials(self):
    self.materials = getMaterials()
    self.MaterialsTableWidget.setRowCount(0)
    
    for index in reversed(self.materials):
      row = [str(item) for item in index]
      self.MaterialsTableWidget.insertRow(0)
      self.MaterialsTableWidget.setItem(0, 0, QTableWidgetItem(row[0]))
      self.MaterialsTableWidget.setItem(0, 1, QTableWidgetItem(row[1]))
      self.MaterialsTableWidget.setItem(0, 2, QTableWidgetItem(row[2]))
      self.MaterialsTableWidget.setItem(0, 3, QTableWidgetItem(row[3]))
      self.MaterialsTableWidget.setItem(0, 4, QTableWidgetItem(row[4]))
      self.MaterialsTableWidget.setItem(0, 5, QTableWidgetItem(row[5]))

  #def showError(self, message):
  #  msg = QMessageBox()
  #  msg.setIcon(QMessageBox.Critical)
  #  msg.setText("Ошибка")
  #  msg.setInformativeText(message)
  #  msg.setWindowTitle("Ошибка")
  #  msg.setStandardButtons(QMessageBox.Ok)
  #  msg.exec_()
  
  #def showSuccess(self, message):
  #  msg = QMessageBox()
  #  msg.setIcon(QMessageBox.Information)
  #  msg.setText("Успех")
  #  msg.setInformativeText(message)
  #  msg.setWindowTitle("Успех")
  #  msg.setStandardButtons(QMessageBox.Ok)
  #  msg.exec_()