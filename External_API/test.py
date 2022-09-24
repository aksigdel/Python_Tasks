import requests
import json
id=41487
def json_print(obj):
    #dumping= response.json()
    data=json.dumps(obj, indent=4)
    return f"<pre>{json.dumps(data,indent = 4)}</pre>" 
response=requests.get(f'http://127.0.0.1:5000/anime/{id}')
print(json_print(response))
