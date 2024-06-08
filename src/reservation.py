import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()

def new_reservation(rid, json_reserv, token):

    url = f"{environ.get('APIGW_URL')}/rsv/v1/hotels/{rid}/reservations"

    payload = json.dumps(json_reserv)
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': rid,
    'x-app-key': environ.get('APP_KEY'),
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)


def get_reservation_by_id(rid, reservation_id, token):

    url = f"{environ.get('APIGW_URL')}/rsv/v1/hotels/{rid}/reservations/{reservation_id}?fetchInstructions=Reservation&fetchInstructions=Comments"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': rid,
    'x-app-key': environ.get('APP_KEY'),
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return False
