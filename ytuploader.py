import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import glob
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def check_element(xpath):
    try:
        driver.implicitly_wait(1)
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


user_name = open("resources/google_user.txt", "r").readline()
password = open("resources/google_pass.txt", "r").readline()

pyautogui.FAILSAFE = False

visibility = 3 ### 1 = PUBLIC
               ### 2 = UNLISTED
               ### 3 or anything else = PRIVATE

###=====MAIN=====###

print('Opening browser')
driver = webdriver.Chrome(service_log_path='logs/geckodriver.log')
driver.get('https://www.youtube.com')

driver.implicitly_wait(60)
driver.find_element_by_xpath("/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a/paper-button").click()

print('Logging in')
driver.implicitly_wait(60)
driver.find_element_by_id('identifierId').send_keys(user_name)
time.sleep(2)
driver.find_element_by_id('identifierNext').click()
time.sleep(2)
driver.implicitly_wait(60)
driver.find_element_by_name('password').send_keys(password)
time.sleep(2)
driver.find_element_by_id('passwordNext').click()


time.sleep(5)
driver.get('https://studio.youtube.com')
print('Logged in')

for file in sorted(glob.glob("videos\\*.mp4"), key=numericalSort):

    if not file:
        break

    print('')
    print('File: ' + file)


    ### CREATE/UPLOAD, WAIT FOR PAGE TO APPEAR
    driver.implicitly_wait(60)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-button").click()
    time.sleep(1)
    driver.implicitly_wait(60)
    driver.find_element_by_xpath("/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-text-menu/paper-dialog/paper-listbox/paper-item[1]/ytcp-ve/div/div/yt-formatted-string").click()
    time.sleep(1)

    ### SELECT FILES
    print('Selecting file')
    driver.implicitly_wait(60)
    driver.find_element_by_xpath("/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-uploads-file-picker/div/ytcp-button/div").click()

    ### INPUT FILE PATH
    absolute_path = os.path.abspath(file)
    time.sleep(6)
    pyautogui.write(absolute_path)
    time.sleep(1)
    pyautogui.press('enter')
    print('File path input done')

    ### TITTLE
    driver.implicitly_wait(60)
    video_title = file.replace("videos\\", "")
    video_title = video_title.replace(".mp4", "")
    video_title = video_title.replace(";", ":")
    video_title = video_title[4:]
    input_title = driver.find_element_by_id('textbox')
    input_title.click()
    time.sleep(0.5)
    input_title.clear()
    input_title.send_keys(video_title)
    print('Adding title: ' + video_title)
    time.sleep(1)

    ### KIDS?
    driver.implicitly_wait(60)
    driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-form-audience/ytcp-audience-picker/div[4]/paper-radio-group/paper-radio-button[2]/div[2]').click()
    time.sleep(1)
    print('Selected: Not for kids')

    ### NEXT BUTTON X2
    driver.implicitly_wait(60)
    driver.find_element_by_id('next-button').click()
    time.sleep(1)
    driver.implicitly_wait(60)
    driver.find_element_by_id('next-button').click()
    time.sleep(1)

    if visibility == 1: ### PUBLIC BUTTON
        driver.implicitly_wait(60)
        driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[1]/paper-radio-group/paper-radio-button[3]/div[2]').click()
        print('Visibility: Public')
        time.sleep(1)
    elif visibility == 2: ### UNLISTED BUTTON
        driver.implicitly_wait(60)
        driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[1]/paper-radio-group/paper-radio-button[2]/div[2]').click()
        print('Visibility: Unlisted')
        time.sleep(1)
    else: ### PRIVATE BUTTON
        driver.implicitly_wait(60)
        driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[1]/paper-radio-group/paper-radio-button[1]/div[2]').click()
        print('Visibility: Private')
        time.sleep(1)

    ### SAVE BUTTON
    driver.implicitly_wait(60)
    driver.find_element_by_id('done-button').click()
    if visibility == 1:
        print('Press Publish')
    else:
        print('Save')


    ### IF VIDEO PROCESSIND DIALOG APPEARS
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/paper-dialog/div[3]/ytcp-button/div"))
        )
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/paper-dialog/div[3]/ytcp-button/div").click()
        print('Closing uploading notification')
    finally:
        time.sleep(2)

    ### UPLOAD COMPLETE CHECK
    driver.implicitly_wait(1)
    uploads_bar = check_element('/html/body/ytcp-uploads-mini-indicator/ytcp-multi-progress-monitor/paper-dialog/div/button/span')
    if uploads_bar == True:
        print('Waiting for upload to finish')
        upload_complete = False
        while upload_complete == False:
            try:
                element = WebDriverWait(driver, 6000).until(
                    lambda driver: driver.find_elements(By.XPATH,"//*[text()='Upload complete']") or driver.find_elements(By.XPATH,"//*[text()='Uploads complete']")
                )
                upload_complete = True
                print('Upload done')
            except:
                time.sleep(1)
    else:
        print('done')

    # driver.get('https://www.youtube.com/channel/UCfHsgrKGFWHYzP5XPbp4jsQ/videos')

    ### VIDEO PUBLISH CHECK
    # print('Waiting until published')
    # driver.get('https://www.youtube.com/channel/UCfHsgrKGFWHYzP5XPbp4jsQ/videos')
    # video_published = False
    # while video_published == False:
    #     try:
    #         driver.implicitly_wait(1)
    #         driver.find_element_by_xpath("//*[contains(text(), '" + video_title + "')]")
    #         video_published = True
    #         print('Publish done')
    #         time.sleep(10)
    #     except:
    #         time.sleep(7)
    #         driver.get('https://www.youtube.com/channel/UCfHsgrKGFWHYzP5XPbp4jsQ/videos')

    #x = input('press Enter to continue...')
    driver.get('https://studio.youtube.com')
