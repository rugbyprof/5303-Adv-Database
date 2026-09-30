import requests
from rich import print
"""
This file does an example get request from a locally running api that dishes out answers based on the store.db sqlite db

"""


r = requests.get("http://localhost:8001/products?limit=50&offset=50")

print(r.json())