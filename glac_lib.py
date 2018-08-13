import urllib.request, json 

def read(server):
    api_url = {
        's1': 'https://glaca.nostale.club/api/pl/1/',
        's2': 'https://glaca.nostale.club/api/pl/2/',
        's3': 'https://glaca.nostale.club/api/pl/3/',
        's4': 'https://glaca.nostale.club/api/pl/4/',
    }.get(server, None)
    if api_url is not None:
        with urllib.request.urlopen(api_url) as url:
            data = json.loads(url.read().decode())
            return data
    else:
        return None
