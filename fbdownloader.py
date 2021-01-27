# Facebook Private Video Downloader v3 - Python Script
# Vladimi Popovic - Astrov
# Kovin 18-Jan-2021

### using selenium to access web
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from datetime import date
import glob
import re

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def count_number():
    for last_file_published in sorted(glob.glob("D:\\396\\Miran Rubin Video\\published\\*.mp4"), key=numericalSort):
        if not last_file_published:
            break
        last_video_number = last_file_published
    last_video_number = last_video_number.replace("D:\\396\\Miran Rubin Video\\published\\","")
    last_count_number = last_video_number[:3]
    count_number = int(last_count_number) + 1
    return(count_number)

### Function: Log in Facebook
def fb_login():
    print('loging in...')
    user_name = open("resources/fb_user.txt", "r").readline()
    password = open("resources/fb_pass.txt", "r").readline()
    input_email = driver.find_element_by_id("email")
    input_email.send_keys(user_name)
    input_pass = driver.find_element_by_id("pass")
    input_pass.send_keys(password)
    input_email.send_keys(Keys.ENTER)

def download_page_1(page_source, HD):
    driver.get('https://downloadfacebook.net/en/facebook-private-video-downloader.html')
    input_source = driver.find_element_by_id('facebook-private-video')
    driver.execute_script('arguments[0].value=arguments[1]', input_source, page_source)
    submit_button = driver.find_element_by_xpath("/html/body/main/section[1]/div/div/div/div[2]/form/button/span").click()
    try: # HD
        download_button = driver.find_element_by_xpath("/html/body/main/section[2]/div/div[2]/table/tbody/tr[1]/td[5]/a") #HD
        download_url = download_button.get_attribute('href')
    except:
        print("No HD on download page 1.")
        try: # SD
            download_button = driver.find_element_by_xpath("/html/body/main/section[2]/div/div[1]/div[1]/div[2]/a") #SD
            if HD == 2:
                download_url = download_button.get_attribute('href')
            elif HD == 1:
                print('page 1 elif false')
                download_url = False
        except:
            #print('page 1 except false')
            download_url = False
    return download_url

def download_page_2(page_source):
    driver.get('https://getfbstuff.com/facebook-private-video-downloader') # Open Page
    input_source = driver.find_element_by_id('sourceHTML') # Find Box
    driver.execute_script('arguments[0].value=arguments[1]', input_source, page_source) # Paste Source (JavaScript)
    submit_button = driver.find_element_by_xpath("/html/body/section/div/div/div/div[1]/div/form/div/div/center/button").click() # Click First Download button
    try:
        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div/div/div/div/div[2]/p")) #wait for blue box text, just to confirm page load
        )
        dl_button = driver.find_element_by_xpath("div/div/div[1]/div/div[2]/center/a") # Find Second Download Button
        download_url = dl_button.get_attribute('href') # Get Button URL
        return download_url
    except:
        print("No HD on download page 2.")
        if HD == 1:
            download_url = False

        else:
            print ("SD only is available.")

###================== MAIN =================###

HD = 2  ### 1 - only HD, Check 3 pages for HD, if none, script goes to the next URL
        ### 2 - HD or SD - Check 3 pages for HD, if not, then SD

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(service_log_path='logs/geckodriver.log', options=options) #Open page

print('accessing Facebook...')
driver.get('https://www.facebook.com')
facebook_login = fb_login() #FACEBOOK LOGIN FUNCTION
time.sleep(5)

# Scan Url List
urllist = open("resources/video_list.txt", "r")
url = urllist.readline()

count = count_number() # function - get last published number + 1
while url:

    url = url.rstrip("\n") # stripping blank space
    if not url: # break looop if no more lines in file
        break
    countprint = str(count)
    print('')
    print('URL ' + countprint + ': ' + url) # Control print in console (current video in progress)

    driver.get(url) # Open video page
    #time.sleep(2)
    print('getting source')
    page_source = driver.page_source
    #output = file_output(page_source)

    date_posted = date.today() # FIND DATE FUNCTION

    print('attempting to download')
    if HD == 1:
        download_url = download_page_1(page_source, HD) # DOWNLOAD VIDEO PAGE FUNCTION
        if download_url == False:
            download_url = download_page_2(page_source)

    if HD == 2:
        download_method_1 = download_page_1(page_source, HD) # DOWNLOAD VIDEO PAGE FUNCTION
        if download_method_1 != False:
            download_url = download_method_1
        download_method_2 = download_page_2(page_source)
        if download_method_2 != False and download_method_1 == False:
            download_url = download_method_2

    if download_url != False: # Get URL
        print('downloading...')
        r = requests.get(download_url)
        video_name = ("videos/{0}. Miran Rubin - {1}.mp4".format(count, date_posted)) # Naming in Loop
        open(video_name, 'wb').write(r.content) # Save Video
        print("Done: " + "{0}. Miran Rubin - {1}.mp4".format(count, date_posted))

    count += 1 # Increment name index for every loop
    url = urllist.readline()
