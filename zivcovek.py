import os

urllist = open("resources/video_list.txt", "r")
url = urllist.readline()

urllist = open("logs/uploaded.log", "r")
uploaded = urllist.readline()

if url != uploaded:
    exec(open('fbdownloader.py').read())
    exec(open('ytuploader.py').read())

    output_file = open('logs/uploaded.log','w', encoding="utf-8") #save last URL to log chech for double
    print(url, file=output_file)

    exec(open('filemove.py').read())
else:
    print(url + ' already posted on Youtube/Ziv Covek')
