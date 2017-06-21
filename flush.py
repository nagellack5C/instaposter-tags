#flushes database

import sqlite3
from os import listdir, remove, chdir, getcwd
from shutil import rmtree
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

conn = sqlite3.connect('ex1.db')
c = conn.cursor()
c.execute("DELETE FROM imgs WHERE rowid > 0")
conn.commit()
conn.close()

path = r"C:/Users/fatsu/PycharmProjects/Instagram-API-python/"
print(path)
chdir(path)
rmtree(path + "patterndesign")
remove(path + "data.txt")
remove(path + "see.html")
print("Success!")