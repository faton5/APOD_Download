                         #####################################################
                         # Auteur : FATON                                    #
                         # Date : 2021-06-14                                 #
                         # Version : 1.0                                     #
                         #####################################################

import smbclient,requests,os,time
from datetime import datetime, timedelta

# NASA API URL
APOD_URL = "https://api.nasa.gov/planetary/apod"

# Request the necessary information from the user
API_KEY = input("Enter your API key : ")
START_DATE = datetime(1995, 6, 16)
REQUESTS_PER_HOUR = 1000

# Ask users whether they want to download images locally or from the network
download_location = input("Do you want to download images locally or over the network? (local/network) : ")

if download_location == 'network':
    SERVER = input("Enter the server name : ")
    USERNAME = input("Enter user name : ")
    PASSWORD = input("Enter password : ")
    SAVE_PATH = input("Enter the path to save images on the network : ")
    LOG_PATH = input("Enter the path of the log file on the network : ")
    smbclient.register_session(SERVER, username=USERNAME, password=PASSWORD)
elif download_location == 'local':
    SAVE_PATH = input("Enter the path to save images locally : ")
    LOG_PATH = input("Enter the path of the log file locally : ")

def download_image(date):
    response = requests.get(APOD_URL, params={'api_key': API_KEY, 'date': date.strftime('%Y-%m-%d')})
    data = response.json()
    if 'url' in data and data['media_type'] == 'image':
        image_url = data['url']
        image_response = requests.get(image_url)
        image_name = os.path.join(SAVE_PATH, date.strftime('%Y-%m-%d') + '.jpg')
        if download_location == 'local':
            with open(image_name, 'wb') as f:
                f.write(image_response.content)
        else:
            with smbclient.open_file(f"\\\\{SERVER}\\{SAVE_PATH}\\{image_name}", mode='wb') as f:
                f.write(image_response.content)
        print(f"Downloaded image : {image_name}")
    else:
        with open('images_not_downloaded.txt', 'a') as f:
            f.write(f"{date.strftime('%Y-%m-%d')}\n")

def write_log(message):
    if download_location == 'local':
        with open(LOG_PATH, 'a') as f:
            f.write(f"{message}\n")
    else:
        with smbclient.open_file(f"\\\\{SERVER}\\{LOG_PATH}", mode='a') as f:
            f.write(f"{message}\n")

current_date = START_DATE
requests_this_hour = 0
start_time = time.time()

while True:
    if current_date > datetime.now():
        time.sleep(3600)  # Wait for 1 hour if we've reached the current date
        continue

    download_image(current_date)
    write_log(f"Image for {current_date.strftime('%Y-%m-%d')} downloaded")
    current_date += timedelta(days=1)
    requests_this_hour += 1

    if requests_this_hour >= REQUESTS_PER_HOUR:
        time_to_next_hour = 3600 - (time.time() - start_time)
        if time_to_next_hour > 0:
            time.sleep(time_to_next_hour)  # Wait until the next hour if we've reached the request limit
        start_time = time.time()
        requests_this_hour = 0