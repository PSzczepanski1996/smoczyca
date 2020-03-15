import json
import urllib.request


def read(server):
    api_url = {
        's1': 'https://glaca.nostale.club/api/pl/1/',
    }.get(server, None)
    if api_url is not None:
        with urllib.request.urlopen(api_url) as url:
            data = json.loads(url.read().decode())
            return data
    return None
