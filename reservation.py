import requests
import json

def new_reservation(rid, json_reserv, token):

    url = f"https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/rsv/v1/hotels/{rid}/reservations"

    payload = json.dumps(json_reserv)
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': rid,
    'x-app-key': '5502014f-a4f1-4135-9d45-ae5fd594eba5',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)


def get_reservation_by_id(rid, reservation_id, token):

    url = f"https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/rsv/v1/hotels/{rid}/reservations/{reservation_id}?fetchInstructions=Reservation&fetchInstructions=Comments"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': rid,
    'x-app-key': '5502014f-a4f1-4135-9d45-ae5fd594eba5',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return False
