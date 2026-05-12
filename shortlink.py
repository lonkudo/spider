import requests

TOKEN = '283f0a2e0b60f47774fbbc4979a537e6516e51d8'
BITLY_API = 'https://api-ssl.bitly.com/v4/'

def shorten_link(long_url):
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {'long_url': long_url}
    r = requests.post(BITLY_API + 'shorten', json=data, headers=headers)
    return r.json()

def get_clicks(bitlink):
    headers = {'Authorization': f'Bearer {TOKEN}'}
    r = requests.get(BITLY_API + f'bitlinks/{bitlink}/clicks/summary', headers=headers)
    return r.json()

# Usage
short = shorten_link("https://example.com")
print(short["link"])  # shortened URL

clicks = get_clicks(short["id"].replace("https://", ""))
print(clicks["total_clicks"])
