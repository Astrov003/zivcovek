import os

print('starting script')
urllist = open("/home/vladimir/resources/video_list.txt", "r")
uploading_url = urllist.readline()
uploading_url = uploading_url.replace('\n', '')

urllist2 = open("logs/uploaded.log", "r")
uploaded_url = urllist2.readline()
uploaded_url = uploaded_url.replace('\n', '')


if uploading_url != uploaded_url:
    exec(open('fbdownloader.py').read())
    exec(open('filemove.py').read())
else:
    print("<" + uploading_url + ">" + ' already posted on Youtube/Ziv Covek')
