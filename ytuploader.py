import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import glob
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import os.path

JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver = element.parent
    isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths = []

    # ensure files are present, and upload to the remote server if session is remote
    for file in (files if isinstance(files, list) else [files]) :
        if not os.path.isfile(file) :
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))

    value = '\n'.join(paths)
    elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})

WebElement.drop_files = drop_files

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

print('accessing YouTube')

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(service_log_path='logs/geckodriver.log', options=options) #Open page

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
    dropzone = driver.find_element_by_xpath("/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-uploads-file-picker/div/ytcp-button/div")#.click()
    absolute_path = os.path.abspath(file)
    dropzone.drop_files(absolute_path)

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
        #print('Closing uploading notification')
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
