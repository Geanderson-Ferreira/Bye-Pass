import requests

permissions = {
    "integracao_geanderson": ["H5633", "H9360"],
    "anne.cardoso": ["H5519"]
}

def auth(user, password):

    url = "https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/oauth/v1/tokens"

    payload = f'username={user}&password={password}&grant_type=password'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'x-app-key': '5502014f-a4f1-4135-9d45-ae5fd594eba5',
    'Authorization': 'Basic QUNDT1JBVF9DbGllbnQ6eWJRWDV4by1iS1dKVFhYcHBVamZULWxS'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200 and user in permissions.keys():
        return {"token": response.json()['access_token'], "rid": permissions[user]}
    else:
        return False
    