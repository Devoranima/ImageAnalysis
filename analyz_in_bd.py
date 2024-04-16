# Анализ материала
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout


class MaterialAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализатор материалов")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Создание выпадающего списка
        self.material_combobox = QComboBox()
        self.populate_materials()
        layout.addWidget(self.material_combobox)

        # Создание меток для отображения характеристик
        self.pore_area_label = QLabel()
        layout.addWidget(self.pore_area_label)

        self.pore_area_deviation_label = QLabel()
        layout.addWidget(self.pore_area_deviation_label)

        self.porosity_label = QLabel()
        layout.addWidget(self.porosity_label)

        self.porosity_deviation_label = QLabel()
        layout.addWidget(self.porosity_deviation_label)

        self.setLayout(layout)

        # Подключение сигнала выбора элемента к слоту для обновления информации
        self.material_combobox.currentIndexChanged.connect(self.show_characteristics)

    def populate_materials(self):
        # Подключение к базе данных
        conn = sqlite3.connect('СППР.db')
        cur = conn.cursor()

        # Создание таблицы, если она не существует
        cur.execute("""CREATE TABLE IF NOT EXISTS Materials (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        PORE_AREA REAL NOT NULL,
                        PORE_AREA_DEVIATION REAL NOT NULL,
                        POROSITY REAL NOT NULL,
                        POROSITY_DEVIATION REAL NOT NULL
                        )""")

        # Вставка данных, если таблица пуста
        cur.execute("SELECT COUNT(*) FROM Materials")
        if cur.fetchone()[0] == 0:
            rows = [
                ('Материал1', 12.0, 5.0, 0.1, 0.01),
                ('Материал2', 9.00, 8.0, 0.15, 0.01),
                ('Материал3', 15.0, 8.0, 0.2, 0.5),
                ('Материал4', 14.0, 7.0, 0.3, 0.7),
            ]
            cur.executemany("""INSERT INTO Materials (NAME, PORE_AREA, PORE_AREA_DEVIATION, POROSITY, POROSITY_DEVIATION)
                               VALUES (?, ?, ?, ?, ?)""", rows)

            conn.commit()

        # Получение списка материалов из базы данных и добавление их в выпадающий список
        cur.execute("SELECT NAME FROM Materials")
        materials = cur.fetchall()
        for material in materials:
            self.material_combobox.addItem(material[0])

        conn.close()

    def show_characteristics(self):
        selected_material = self.material_combobox.currentText()

        # Подключение к базе данных
        conn = sqlite3.connect('СППР.db')
        cur = conn.cursor()

        # Получение характеристик выбранного материала
        cur.execute("SELECT PORE_AREA_MEAN, PORE_AREA_STD, POROUS_MEAN, POROUS_STD FROM Materials WHERE NAME=?", (selected_material,))
        row = cur.fetchone()
        if row:
            self.pore_area_label.setText(f"Площадь поры: {row[0]}")
            self.pore_area_deviation_label.setText(f"Откл. от площади: {row[1]}")
            self.porosity_label.setText(f"Пористость: {row[2]}")
            self.porosity_deviation_label.setText(f"Откл. от пористости: {row[3]}")

        conn.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MaterialAnalyzer()
    window.show()
    sys.exit(app.exec_())