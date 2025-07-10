import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from urllib.parse import quote

# === CONFIG ===
SWITCHBOT_TOKEN = os.environ("SWITCHBOT_TOKEN")
DEVICE_ID = os.environ("DEVICE_ID")
WOW_SITE_ID = os.environ("WOW_SITE_ID")
WOW_API_KEY = os.environ("WOW_API_KEY")

# === Step 1: Fetch data from SwitchBot ===
def get_switchbot_data():
    headers = {
        'Authorization': SWITCHBOT_TOKEN
    }
    url = f'https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/status'
    response = requests.get(url, headers=headers)
    data = response.json()['body']
    temperature = data.get('temperature')
    temperature = (temperature * 9/5) + 32
    humidity = data.get('humidity')
    return temperature, humidity

# === Step 2: Format data for WOW ===
def format_wow_payload(temp, humid):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    encoded_timestamp = quote(timestamp)
    payload = {
        'siteid': WOW_SITE_ID,
        'siteAuthenticationKey': WOW_API_KEY,
        'dateutc': encoded_timestamp,
        'tempf': temp,
        'humidity': humid,
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
    temp, humid = get_switchbot_data()
    wow_payload = format_wow_payload(temp, humid)
    upload_to_wow(wow_payload)