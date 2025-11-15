import requests
import json

query = 'hacking'
url = f'https://api.duckduckgo.com/?q={query}&format=json'

response = requests.get(url)
data = response.json()

print(json.dumps(data, indent=2))
