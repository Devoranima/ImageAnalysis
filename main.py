
#task9
# Редактор бд
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class DatabaseEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор базы данных")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица с данными
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Наименование", "Площадь поры", "Откл. от площади", "Пористость", "Откл. от пористости"])
        layout.addWidget(self.table)

        # Поля для ввода новой записи
        add_record_layout = QHBoxLayout()
        self.text_edit_material_name = QLineEdit()
        self.text_edit_material_name.setPlaceholderText("Наименование")
        self.text_edit_material_area = QLineEdit()
        self.text_edit_material_area.setPlaceholderText("Площадь поры")
        self.text_edit_material_area_std = QLineEdit()
        self.text_edit_material_area_std.setPlaceholderText("Откл. от площади")
        self.text_edit_material_porous = QLineEdit()
        self.text_edit_material_porous.setPlaceholderText("Пористость")
        self.text_edit_material_porous_std = QLineEdit()
        self.text_edit_material_porous_std.setPlaceholderText("Откл. от пористости")
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.push_button_add_click)
        add_record_layout.addWidget(self.text_edit_material_name)
        add_record_layout.addWidget(self.text_edit_material_area)
        add_record_layout.addWidget(self.text_edit_material_area_std)
        add_record_layout.addWidget(self.text_edit_material_porous)
        add_record_layout.addWidget(self.text_edit_material_porous_std)
        add_record_layout.addWidget(add_button)
        layout.addLayout(add_record_layout)

        # Поля для изменения значений
        edit_record_layout = QHBoxLayout()
        self.text_edit_id = QLineEdit()
        self.text_edit_id.setPlaceholderText("ID записи")
        self.text_edit_area = QLineEdit()
        self.text_edit_area.setPlaceholderText("Новая площадь поры")
        self.text_edit_area_std = QLineEdit()
        self.text_edit_area_std.setPlaceholderText("Новое откл. от площади")
        self.text_edit_porous = QLineEdit()
        self.text_edit_porous.setPlaceholderText("Новая пористость")
        self.text_edit_porous_std = QLineEdit()
        self.text_edit_porous_std.setPlaceholderText("Новое откл. от пористости")
        edit_button = QPushButton("Изменить")
        edit_button.clicked.connect(self.push_button_edit_click)
        edit_record_layout.addWidget(self.text_edit_id)
        edit_record_layout.addWidget(self.text_edit_area)
        edit_record_layout.addWidget(self.text_edit_area_std)
        edit_record_layout.addWidget(self.text_edit_porous)
        edit_record_layout.addWidget(self.text_edit_porous_std)
        edit_record_layout.addWidget(edit_button)
        layout.addLayout(edit_record_layout)

        # Поле для удаления записей
        delete_layout = QHBoxLayout()
        self.text_edit_delete_id = QLineEdit()
        self.text_edit_delete_id.setPlaceholderText("ID записи для удаления")
        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.push_button_delete_click)
        delete_layout.addWidget(self.text_edit_delete_id)
        delete_layout.addWidget(delete_button)
        layout.addLayout(delete_layout)

        # Блок с кнопкой "OK"
        button_layout = QHBoxLayout()
        save_button = QPushButton("OK")
        save_button.setFixedSize(100, 30)
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(save_button, alignment=Qt.AlignRight)  # Выравниваем по правому краю

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Создание таблицы и загрузка данных из базы данных
        self.create_table()
        self.load_materials()

    def create_table(self):
        # Подключение к базе данных
        conn = sqlite3.connect('СППР.db')
        cur = conn.cursor()

        # Создание таблицы Materials, если она не существует
        cur.execute("""CREATE TABLE IF NOT EXISTS Materials (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        PORE_AREA_MEAN REAL NOT NULL,
                        PORE_AREA_STD REAL NOT NULL,
                        POROUS_MEAN REAL NOT NULL,
                        POROUS_STD REAL NOT NULL
                        )""")

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()


    def load_materials(self):
        conn = sqlite3.connect('СППР.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Materials")
        data = cur.fetchall()

        # Заполнение таблицы данными
        self.table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_num, col_num, item)

        # Закрытие соединения
        conn.close()

    def push_button_add_click(self):
        material_name = self.text_edit_material_name.text()
        material_area = self.text_edit_material_area.text()
        material_area_std = self.text_edit_material_area_std.text()
        material_porous = self.text_edit_material_porous.text()
        material_porous_std = self.text_edit_material_porous_std.text()

        # Проверка наличия данных
        if material_name and material_area and material_area_std and material_porous and material_porous_std:
            try:
                material_area = float(material_area)
                material_area_std = float(material_area_std)
                material_porous = float(material_porous)
                material_porous_std = float(material_porous_std)

                conn = sqlite3.connect('СППР.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO Materials (NAME, PORE_AREA_MEAN, PORE_AREA_STD, POROUS_MEAN, POROUS_STD) VALUES (?, ?, ?, ?, ?)",
                            (material_name, material_area, material_area_std, material_porous, material_porous_std))
                conn.commit()
                conn.close()

                # Обновление данных в таблице
                self.load_materials()
            except ValueError:
                print("Ошибка: неверный формат числа.")
        else:
            print("Ошибка: заполните все поля.")

    def push_button_edit_click(self):
        material_id = self.text_edit_id.text()
        area = self.text_edit_area.text()
        area_std = self.text_edit_area_std.text()
        porous = self.text_edit_porous.text()
        porous_std = self.text_edit_porous_std.text()

        # Проверка наличия данных
        if material_id and area and area_std and porous and porous_std:
            try:
                # Преобразование в целые числа
                material_id = int(material_id)
                area = float(area)
                area_std = float(area_std)
                porous = float(porous)
                porous_std = float(porous_std)

                # Подключение к базе данных и обновление записи
                conn = sqlite3.connect('СППР.db')
                cur = conn.cursor()
                cur.execute("UPDATE Materials SET PORE_AREA_MEAN=?, PORE_AREA_STD=?, POROUS_MEAN=?, POROUS_STD=? WHERE ID=?",
                            (area, area_std, porous, porous_std, material_id))
                conn.commit()

                # Загрузка обновленных данных
                self.load_materials()
            except ValueError:
                print("Ошибка: неверный формат ID или значения.")
        else:
            print("Ошибка: заполните все поля.")

    def push_button_delete_click(self):
        material_id = self.text_edit_delete_id.text()

        if material_id:
            try:
                material_id = int(material_id)

                # Подключение к базе данных и удаление записи
                conn = sqlite3.connect('СППР.db')
                cur = conn.cursor()
                cur.execute("DELETE FROM Materials WHERE ID=?", (material_id,))
                conn.commit()

                # Загрузка обновленных данных
                self.load_materials()
            except ValueError:
                print("Ошибка: неверный формат ID.")
        else:
            print("Ошибка: введите ID записи для удаления.")

    def save_changes(self):
        print("Изменения сохранены")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseEditor()
    window.show()
    sys.exit(app.exec_())
