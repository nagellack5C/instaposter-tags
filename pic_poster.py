from InstagramAPI import InstagramAPI
import sqlite3
import os

print(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

################CREDENTIALS################
login = "login"
password = "pass"
################CREDENTIALS################

################PREDEFINED################
pic_dir = "C:/Users/fatsu/PycharmProjects/Instagram-API-python/patterndesign/"
################PREDEFINED################

InstagramAPI = InstagramAPI(login, password)
InstagramAPI.login()



def load_new_photo(dir_path):
    conn = sqlite3.connect('ex1.db')
    c = conn.cursor()
    query = "SELECT * FROM imgs ORDER BY ROWID ASC LIMIT 1"
    result = c.execute(query)
    fetched_item = []
    for row in result:
        fetched_item = row
    #edit caption parameter for custom caption text
    InstagramAPI.uploadPhoto(dir_path + fetched_item[2] + ".jpg", caption="@" + fetched_item[1])
    query = "DELETE FROM imgs WHERE url = '" + fetched_item[0] + "'"
    c.execute(query)
    conn.commit()
    conn.close()


load_new_photo(pic_dir)

#if you need to see the output in the terminal/cmd
#print("Photo downloaded successfull! Press Enter to quit")
#x = input()