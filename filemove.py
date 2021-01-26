import os
import glob
import re
import shutil

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for file in sorted(glob.glob("test\\*.mp4"), key=numericalSort):

    if not file:
        break
    video_number = os.path.abspath(file)

print(video_number)
video_number = video_number.replace(file, "")
print(video_number)
# video_number = video_number[:10]
# video_number = video_number[-3:]
# count_number = int(video_number) + 1
#
# file_name = file.replace("videos\\", "")
# file_name = file_name[3:]
# #print('Video: ' + file + ' renamed to: ' + str(file_name))
# os.rename(file, "test\\" + str(count_number) + file_name)
