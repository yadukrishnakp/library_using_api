import requests

BASE = "http://127.0.0.1:5000/"


response=requests.put(BASE + "library/naalukettu", {"name": "naalukettu", "author": "M.T. Vasudevan Nair", "stocks": 9, "price": 355})
print(response.json())