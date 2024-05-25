import sqlite3


def getMaterials():
  """Фунция для получения материалов из базы данных
  """
  conn = sqlite3.connect("db/ImageAnalysis")
  cur = conn.cursor()
  cur.execute("SELECT * FROM Materials ORDER BY ID ASC;")
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows


def deleteMaterial(id):
  """Фунция для удаления материала из базы данных
  """
  conn = sqlite3.connect("db/ImageAnalysis")
  cur = conn.cursor()
  cur.execute('DELETE FROM Materials WHERE ID=?',
  (id,))
  conn.commit()
  conn.close()


def addMaterial(name, square, squareDeviation, porosity, porosityDeviation):
  """Фунция для добавления материала в базу данных
  """
  conn = sqlite3.connect("db/ImageAnalysis")
  cur = conn.cursor()
  cur.execute('INSERT INTO Materials (NAME, PORE_AREA_MEAN, PORE_AREA_STD, POROUS_MEAN, POROUS_STD) VALUES (?, ?, ?, ?, ?)',
  (name, square, squareDeviation, porosity, porosityDeviation))
  conn.commit()
  conn.close()