import json

with open("events.json") as f:
    data = f.read()

data = json.loads(data)

print(data)