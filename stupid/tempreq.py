import requests


r = requests.get("http://localhost:8001/products?limit=50&offset=0")

print(r.json())