import requests
import json

blockData = {'block': {'id': '79d2421c82c88bc3b786a70a03209d939b9853e4cec0078bd4cd226fe4ad3a79', 'index': 4, 'gindex': 1, 'timestamp': 1570415888.272096, 'transactions': '280185ceda22d90da98cb0e48993c5d11fc5063675536b007350c0cb9dc31593', 'proof': 1649, 'previous_hash': '0007bbacd87086021868e220a20a0cbd620a83959c1eef2de22b2447f6013fcb', 'previous_g_hash': '4f025c4ef95f64c069dc448b3aef548332f0db12ef7567ff8fa345bd16fe8f11'}, 'gpointer': []}
try:
    # res = requests.get("http://localhost:5000/get_index")
    requests.post("http://localhost:5000/addGlobalBlock", json = blockData)
except :
    print("1")
    pass


# print( json.loads(str(res.content,"utf-8")))