import requests
import json

from config import Config


def get_state_order(token, id_client):

    url = f"{Config.base_url}/order/state"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {"id_client": id_client}

    # Serialize data dictionary to JSON
    json_data = json.dumps(data)

    response = requests.post(url, headers=headers, data=json_data)

    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code
