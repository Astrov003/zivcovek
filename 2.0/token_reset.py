# Facebook Private Video Downloader v2 - Python Script
# Vladimir Popovic - Astrov
# Kovin 18-Jan-2021

### using selenium to access web
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from selenium.webdriver.chrome.options import Options
from datetime import date
import glob
import re

HD = 2  ### 1 - only HD, Check 3 pages for HD, if none, script goes to the next URL
        ### 2 - HD or SD - Check 3 pages for HD, if not, then SD

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def count_number():
    for last_file_published in sorted(glob.glob("/mnt/storage1/Živ Čovek/Miran Rubin Video/12. Miran - Maj, 2021/*.mp4"), key=numericalSort):
        if not last_file_published:
            print('corak')
            break
        last_video_number = last_file_published
    last_video_number = last_video_number.replace("/mnt/storage1/Živ Čovek/Miran Rubin Video/12. Miran - Maj, 2021/","")

    last_count_number = last_video_number[:3]
    count_number = int(last_count_number) + 1
    return(count_number)

### Function: Log in Facebook
def fb_login():
    print('logging in...')
    user_name = open("/home/vladimir/resources/fb_user.txt", "r").readline()
    user_name = user_name.rstrip("\n")
    password = open("/home/vladimir/resources/fb_pass.txt", "r").readline()
    password = password.rstrip("\n")
    input_email = driver.find_element_by_id("email")
    input_email.send_keys(user_name)
    input_pass = driver.find_element_by_id("pass")
    input_pass.send_keys(password)
    input_email.send_keys(Keys.ENTER)


###================== MAIN =================###

#count = count_number() # function - get last published number + 1

print('Input 1.video 2.number code 3. read from txt list: ')
choice = input()

if choice == '1':
    url = input()
elif choice == '2':    
    video_number_code = input()
    url = 'https://www.facebook.com/miranrubin/videos/' + str(video_number_code)
    print('URL ' + str(count) + ': ' + str(url))
elif choice == '3':
    # Scan Url List
    urllist = open("/home/vladimir/resources/video_list.txt", "r")
    url = urllist.readline()
    print(url)
    
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(service_log_path='logs/geckodriver.log', options=options) #Open page

print('accessing Facebook...')
driver.get('https://www.facebook.com')
facebook_login = fb_login() #FACEBOOK LOGIN FUNCTION
time.sleep(5)


while url != 0:
    count = count_number() # function - get last published number + 1

    url = url.rstrip("\n") # stripping blank space
    if not url: # break looop if no more lines in file
        break
    countprint = str(count)
    print('')
    #print('URL ' + countprint + ': ' + url) # Control print in console (current video in progress)

    driver.get(url) # Open video page
    #time.sleep(2)
    print('getting source')
    page_source = driver.page_source
    #output = file_output(page_source)
    # source_write = open("resources/video_source.txt", "a")
    # bla = source_write.write(page_source)


    date_posted = date.today() # FIND DATE FUNCTION

    print('attempting to download')
    #if HD == 1:
        #code

    if HD == 2:

        try:
            found = re.search('"playable_url":"(.+?)"', page_source).group(1) #search between characters, (.+?) je razdelnik
            video_url = found.replace("\\","")
            video_url = video_url.replace("u0025","%")
        except AttributeError:
            print('Error getting url.')
        
    url_output = open("/home/vladimir/resources/video_url.txt", "a")
    url_write = url_output.write(video_url)

    if video_url != False:
        print('downloading...')
        r = requests.get(video_url)
        video_name = ("videos/{0}. Miran Rubin - {1}.mp4".format(count, date_posted)) # Naming in Loop
        print('saving')
        open(video_name, 'wb').write(r.content) # Save Video
        print("Done: " + "{0}. Miran Rubin - {1}.mp4".format(count, date_posted))
   
    url = 0
    if choice == '3':
        exec(open('filemove.py').read())
        url = urllist.readline()
