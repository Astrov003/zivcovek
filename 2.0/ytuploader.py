from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import glob
import re

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

CLIENT_SECRET_FILE = '/home/vladimir/scripts/resources/client_secret_Ziv_Covek.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

title = 'miran rubin - test'

for file in sorted(glob.glob("videos/*.mp4"), key=numericalSort):
    if not file:
        break
    print('')
    print('File: ' + file)

    video_title = file.replace("videos/", "")
    video_title = video_title.replace(".mp4", "")
    video_title = video_title.replace(";", ":")
    video_title = video_title[4:]
    
    video_description =  "=== Miran lajv prenose drži isključivo na Fejsbuku, a ovaj kanal za njega održavaju oni koji prate njegov rad. Miran ne odgovara na Jutjubu. ===\nKupite mi kafu: https://www.buymeacoffee.com/vladimirpl  :::Pozdrav, dragi ljudi. Moje ime je Vladimir. Održavam kanal Živ Čovek za Mirana. Trenutno nemam drugih prihoda, pa ako želite, kupite mi kafu  da mi pomognete u održavanju kanala kako bi nastavio da širi ljubav i istinu!\nHvala od srca!\n\nTekući račun: \n160-5800100502326-44, Banca Intesa\nVladimir Popović\n\nPayPal: vpopovic003@gmail.com\n\n(donacija ne ide Miranu, već meni kao pomoć, uz Miranovu dozvolu)"

    request_body = {
        'snippet':{
            'categoryId': 19,
            'title': video_title,
            'description' : video_description,
        },
        'status': {
            'privacyStatus': 'unlisted',
        }
    }

    mediaFile = MediaFileUpload(file, chunksize=-1, resumable=True)

    response_upload = service.videos().insert(
        part = 'snippet, status',
        body = request_body,
        media_body = mediaFile
    ).execute()
