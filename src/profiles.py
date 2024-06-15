import requests
from os import environ
from dotenv import load_dotenv

load_dotenv()

def get_profile_by_id(prof_id, token, hotel_id):

    url = f"{environ.get('APIGW_URL')}/crm/v1/profiles/{prof_id}?fetchInstructions=Address&fetchInstructions=Comment&fetchInstructions=Communication&fetchInstructions=Correspondence&fetchInstructions=DeliveryMethods&fetchInstructions=FutureReservation&fetchInstructions=GdsNegotiatedRate&fetchInstructions=HistoryReservation&fetchInstructions=Indicators&fetchInstructions=Keyword&fetchInstructions=Membership&fetchInstructions=NegotiatedRate&fetchInstructions=Preference&fetchInstructions=Profile&fetchInstructions=Relationship&fetchInstructions=SalesInfo&fetchInstructions=Subscriptions&fetchInstructions=WebUserAccount"

    payload = {}
    headers = {
    'x-app-key': environ.get('APP_KEY'),
    'x-hotelid': hotel_id,
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return False

def update_profile():
    pass