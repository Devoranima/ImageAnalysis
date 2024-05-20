import numpy as np
# import cv2
import sqlite3
import PIL.Image as Img
import PIL.ImageEnhance as Enhance
import sys

rows = [
 (0, 'Материал2', 12.0, 5.0, 0.1, 0.01),
 (1, 'Материал3', 9.00, 8.0, 0.15, 0.01),
 (2, 'Материал4', 15.0, 8.0, 0.2, 0.5),
 (3, 'Материал5', 14.0, 7.0, 0.3, 0.7),
]
conn = sqlite3.connect("db/ImageAnalysis")
cur = conn.cursor()
cur.executemany("""INSERT INTO Materials values
(?,?,?,?,?,?)""", rows)
conn.commit()
conn.close()
