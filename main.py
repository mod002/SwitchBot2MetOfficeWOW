import requests
import os
import math
from datetime import datetime, timezone
from dotenv import load_dotenv
from urllib.parse import quote

# === CONFIG ===
SWITCHBOT_TOKEN = os.getenv("SWITCHBOT_TOKEN")
DEVICE_ID = os.getenv("DEVICE_ID")
WOW_SITE_ID = os.getenv("WOW_SITE_ID")
WOW_API_KEY = os.getenv("WOW_API_KEY")

# === Step 1: Fetch data from SwitchBot ===
def get_switchbot_data():
    headers = {
        'Authorization': SWITCHBOT_TOKEN
    }
    url = f'https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/status'
    response = requests.get(url, headers=headers)
    data = response.json()['body']
    temperature = data.get('temperature') #temp in C
    humidity = data.get('humidity') #RH
    # Constants for Magnus formula
    a = 17.27
    b = 237.7
    alpha = ((a * temperature) / (b + temperature)) + math.log(humidity / 100.0)
    dewpoint_celsius = (b * alpha) / (a - alpha)
    dewpoint = (dewpoint_celsius * 9/5) + 32
    temperature = (temperature * 9/5) + 32
    return temperature, humidity, dewpoint

# === Step 2: Format data for WOW ===
def format_wow_payload(temp, humid, dewpt):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    encoded_timestamp = quote(timestamp)
    payload = {
        'siteid': WOW_SITE_ID,
        'siteAuthenticationKey': WOW_API_KEY,
        'dateutc': encoded_timestamp,
        'tempf': temp,
        'humidity': humid,
        'dewptf' : dewpt,
        'softwaretype':"SwitchBot2MetOfficeWOW"
    }
    return payload

# === Step 3: Send data to Met Office WOW ===
def upload_to_wow(payload):
    url = 'https://wow.metoffice.gov.uk/automaticreading'
    response = requests.post(url, data=payload)
    print(f'Upload status: {response.status_code}')
    print(response.text)

# === Main Routine ===
if __name__ == '__main__':
    temp, humid, dewpt = get_switchbot_data()
    wow_payload = format_wow_payload(temp, humid, dewpt)
    upload_to_wow(wow_payload)