import json

file = open('webhookOrder.json',)
data = json.load(file)

# print(data['line_items'][0]['name'])
# print(data['line_items'][0]['price'])

order = {}
products = data['line_items']
for p in products:
    print(p['name'])