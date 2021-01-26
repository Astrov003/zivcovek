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
for file_new in sorted(glob.glob("videos\\*.mp4"), key=numericalSort):
    if not file_new:
        break

    for last_file_published in sorted(glob.glob("D:\\396\\Miran Rubin Video\\published\\*.mp4"), key=numericalSort):
        if not last_file_published:
            break

    video_number = last_file_published
video_number = video_number.replace("D:\\396\\Miran Rubin Video\\published\\","")

count_number = video_number[:3]
count_number_new = int(count_number) + 1

file_name = file_new.replace("videos\\", "")
file_name = file_name.replace(count_number, str(count_number_new))
file_name = file_name[3:]
shutil.move(file_new, "D:\\396\\Miran Rubin Video\\published\\" + str(count_number_new) + file_name)
print('Video: ' + file_new + ' moved to: "D:\\396\\Miran Rubin Video\\published\\' + str(count_number_new) + str(file_name))
