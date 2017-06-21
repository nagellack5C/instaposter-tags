#work in progress
import json
import requests
import vk_requests
import sqlite3

#set your own params here
user_id = 1
expires_in = 86400
app_id = 1
login='email'
password='pass'
phone_number = "+777777777777"
group_id = 1
scope = "manage,photos,messages,docs"
redirect_uri = "http://oauth.vk.com/blank.html"
pic_dir = "C:/Users/fatsu/PycharmProjects/Instagram-API-python/patterndesign/"

#create new api
api = vk_requests.create_api(app_id=app_id,
                             login=login,
                             phone_number=phone_number,
                             groups_ids=group_id,
                             scope=scope,
                             redirect_uri=redirect_uri,
                             password=password,
                             interactive=True)

groups = 1

upload_url = api.photos.getWallUploadServer(group_id=groups)["upload_url"]
print(upload_url)


def load_new_photo(dir_path):
    conn = sqlite3.connect('ex1.db')
    c = conn.cursor()
    query = "SELECT * FROM imgs ORDER BY ROWID ASC LIMIT 1"
    result = c.execute(query)
    fetched_item = []
    for row in result:
        fetched_item = row
    files = {
        #'file1': open(dir_path + fetched_item[2] + ".jpg", 'rb'),
        'file1': "https://icdn.lenta.ru/images/2017/06/15/12/20170615125114817/top7_d8881bcb4e8447e751f3b2f6359ba83f.jpg",
        'file2': '',
        'file3': '',
        'file4': '',
        'file5': '',
    }
    r = requests.post(upload_url, files=files, headers = {"Content-Type":"multipart/form-data"}).json()
    #parsed = json.loads(r)
    print (json.dumps(r, indent=4, sort_keys=True))
    conn.commit()
    conn.close()

load_new_photo(pic_dir)