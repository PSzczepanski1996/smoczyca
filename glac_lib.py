import json
import requests


def read(server):
    api_url = {
        's1': 'https://glaca.nostale.club/api/pl/1/',
    }.get(server, None)
    if api_url is not None:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
    return None
