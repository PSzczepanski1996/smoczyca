import urllib.request, json 

def read():
    with urllib.request.urlopen("https://glaca.nostale.club/api/pl/1/") as url:
        data = json.loads(url.read().decode())
        return data
