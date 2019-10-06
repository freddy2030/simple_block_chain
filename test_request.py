import requests
import json

try:
    res = requests.get("http://localhost:5001/get_index")
except :
    print("1")
    pass

print( json.loads(str(res.content,"utf-8")))