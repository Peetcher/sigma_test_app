import json
import requests
url = "http://127.0.0.1:8000/sigma_filter"
headers = {'content-type': 'application/json'}
with open('example_2.json', 'r') as file:
    json_res = json.load(file)
    result = requests.post(url=url, data=json.dumps(json_res), headers=headers)
    print(result.content)