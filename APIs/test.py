import requests
import json
def json_print(obj):
    data = json.dumps(obj, indent=4)
    print(data)  
id=10
#response=requests.get(f'http://127.0.0.1:5000/users/{id}')
#response=requests.post(f'http://127.0.0.1:5000/users/{id}')
#response=requests.put(f'http://127.0.0.1:5000/users/{id}')
response=requests.delete(f'http://127.0.0.1:5000/users/{id}')
#response=requests.city_count(f'http://127.0.0.1:5000/city_count')

json_print(response.json())

