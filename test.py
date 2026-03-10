import json

with open('xpath.json','r') as f:
    d = json.loads(f.read())
    print(len(d.keys()))