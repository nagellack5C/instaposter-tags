from InstagramAPI import InstagramAPI
import json
import sqlite3
import os
import urllib.request

print(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

################CREDENTIALS################
login = "login"
password = "pass"
##############WRITE TAGS HERE##############
main_tag = "tag"
tags = ["tag1", "tag2", "tag3"]
################END OF TAGS################

#logging in
InstagramAPI = InstagramAPI(login, password)
InstagramAPI.login()

#getting the tagFeed
def tagFeedGet(main_tag):
    global InstagramAPI
    InstagramAPI.tagFeed(main_tag)
    pattern_json = InstagramAPI.LastJson
    with open('data.txt', 'w') as outfile:
        json.dump(pattern_json, outfile, indent=4)
    outfile.close()
    print("tagFeed - success!")

#filter photos by tag
def filterPhotos(tags):
    str_json = ""
    with open('data.txt', 'r') as outfile:
        for i in outfile:
            str_json += i
    outfile.close()
    str_json = json.loads(str_json)
    conn = sqlite3.connect('ex1.db')
    c = conn.cursor()
    for key in ["ranked_items", "items"]:
        for i in str_json[key]:
            img_url = i["image_versions2"]["candidates"][0]["url"]
            if "?" in img_url:
                img_url = img_url.split('?', 1)[0]
            img_url = "'" + img_url + "', "
            img_poster = "'" + i["user"]["username"] + "', "
            try:
                img_tags = i["caption"]["text"]
            except TypeError:
                img_tags = "paint"
            img_id = "'" + i["id"] + "'"
            if any(x in img_tags for x in tags):
                query = "INSERT INTO imgs VALUES (" + img_url + img_poster + img_id + ")"
                c.execute(query)
                print(query)
    conn.commit()
    conn.close()
    print("filter - success!")

#generate html for easy browsing the grabbed images and choosing ones to delete
def genHTML():
    with open('see.html', 'w') as outfile:
        outfile.write("<!DOCTYPE html>\n<html><head><title>choose your destiny</title></head><body>")
        conn = sqlite3.connect('ex1.db')
        c = conn.cursor()
        query = "SELECT url FROM imgs";
        i = 0
        outfile.write("<p>")
        for row in c.execute(query):
            i += 1
            str_row = str(row)
            str_row = str_row[2:len(str_row)-2]
            outfile.write("<img width='300' height='300' src='" + str_row + "'>")
            if i%6 == 0:
                outfile.write("</p><br /><p>")
        outfile.write("</p>")
        conn.commit()
        conn.close()
        outfile.write("</body>")
        outfile.close()
        print("genHTML - success!")

#download pictures to a dir with the main tag name
def savePics():
    conn = sqlite3.connect('ex1.db')
    newpath = 'C:/Users/fatsu/PycharmProjects/Instagram-API-python/' + main_tag + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    c = conn.cursor()
    query = "SELECT url, img_id FROM imgs";
    for row in c.execute(query):
        str_row = str(row[0])
        print(str_row)
        urllib.request.urlretrieve(str_row, newpath + str(row[1]) + ".jpg")
    conn.close()
    print("savePics - success!")

#main flow
tagFeedGet(main_tag)
filterPhotos(tags)
genHTML()
savePics()

#if you need to see the output in the terminal/cmd
#print("End of script. Press enter")
#z = input()