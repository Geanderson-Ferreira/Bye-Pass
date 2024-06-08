import requests
from os import environ
from dotenv import load_dotenv

load_dotenv()

permissions = {
    "integracao_geanderson": ["H5633", "H9360"],
    "anne.cardoso": ["H5519"],
    "rafael.galan": ["H5519"]
}

def auth(user, password):

    url = f"{environ.get("APIGW_URL")}/oauth/v1/tokens"
    print("URL:", url)
    payload = f'username={user}%0A&password={password}&grant_type=password'
    print("PAYLOAD:", payload)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'x-app-key': environ.get('APP_KEY'),
    'Authorization': f'Basic {environ.get("BASIC_AUTH")}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200 and user in permissions.keys():
        return {"token": response.json()['access_token'], "rid": permissions[user]}
    else:
        return False
