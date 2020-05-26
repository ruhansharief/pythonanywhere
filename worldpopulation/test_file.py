import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

ENDPOINT = '/api/get-stats'

data = {
    "city": 'mysore',
    "country": 'australia'
}

#import pdb;pdb.set_trace()
response = requests.get(BASE_URL+ENDPOINT,data=json.dumps(data))

print(response.json())