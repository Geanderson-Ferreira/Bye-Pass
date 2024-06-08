import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()

def get_arrivals(rid, token):

    url = f"{environ.get('APIGW_URL')}/rsv/v1/hotels/{rid}/reservations?expectedArrivals=true&limit=3000"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': rid,
    'x-app-key': environ.get("APP_KEY"),
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return False
