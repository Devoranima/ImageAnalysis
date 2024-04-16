# Выбор материала
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox
import sqlite3

class MaterialSelectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Выбор материала")
        self.setGeometry(100, 100, 300, 100)
        
        self.material_combobox = QComboBox(self)
        self.material_combobox.setGeometry(50, 30, 200, 30)
        
        self.load_materials()
        
    def load_materials(self):
        db_name = "СППР.db"
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("SELECT ID, NAME FROM Materials")
        materials = cur.fetchall()
        conn.close()
        
        for material in materials:
            material_name = material[1]
            self.material_combobox.addItem(material_name)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MaterialSelectionWindow()
    window.show()
    sys.exit(app.exec_())