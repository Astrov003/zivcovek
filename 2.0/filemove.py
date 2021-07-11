import os
import glob
import re
import shutil

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

print('moving file')
for file_new in sorted(glob.glob("videos/*.mp4"), key=numericalSort):
    if not file_new:
        break

    file_name = file_new.replace("videos/", "")

    shutil.move(file_new, "/media/vladimir/Storage/Videos/Miran Rubin/" + file_name)
    print('Video: ' + file_new + ' moved to  /media/vladimir/Storage/Videos/Miran Rubin/')
