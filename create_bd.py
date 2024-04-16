import sqlite3

# Данные для вставки в таблицу
rows = [
    (0, 'Материал2', 12.0, 5.0, 0.1, 0.01),
    (1, 'Материал3', 9.00, 8.0, 0.15, 0.01),
    (2, 'Материал4', 15.0, 8.0, 0.2, 0.5),
    (3, 'Материал5', 14.0, 7.0, 0.3, 0.7),
]

# Подключение к базе данных
conn = sqlite3.connect('СППР.db')
cur = conn.cursor()

# Создание таблицы Materials
cur.execute("""CREATE TABLE IF NOT EXISTS Materials (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT,
                PORE_AREA_MEAN REAL NOT NULL,
                PORE_AREA_STD REAL NOT NULL,
                POROUS_MEAN REAL NOT NULL,
                POROUS_STD REAL NOT NULL
                )""")

# Вставка данных в таблицу
cur.executemany("""INSERT INTO Materials (ID, NAME, PORE_AREA_MEAN, PORE_AREA_STD, POROUS_MEAN, POROUS_STD)
                   VALUES (?, ?, ?, ?, ?, ?)""", rows)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()