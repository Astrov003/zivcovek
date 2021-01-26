import os

urllist = open("resources/video_list.txt", "r")
uploading_url = urllist.readline()
uploading_url = uploading_url.replace('\n', '')

urllist2 = open("logs/uploaded.log", "r")
uploaded_url = urllist2.readline()
uploaded_url = uploaded_url.replace('\n', '')


if uploading_url != uploaded_url:
    exec(open('fbdownloader.py').read())
    exec(open('ytuploader.py').read())

    output_file = open('logs/uploaded.log','w', encoding="utf-8") #save last URL to log chech for double
    print(uploading_url, file=output_file)

    exec(open('filemove.py').read())
else:
    print("<" + uploading_url + ">" + ' already posted on Youtube/Ziv Covek')
