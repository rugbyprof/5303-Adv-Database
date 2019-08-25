import json
from pprint import pprint

keys = []

with open('asins.json') as data_file:    
    data = json.load(data_file)

for a in data:
    keys.extend(a)

asins = list(set(keys))

pprint(asins)