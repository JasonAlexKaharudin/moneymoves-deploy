import json
import decimal

file = open('webhookOrder.json',)
data = json.load(file)


order = {}
products = data['line_items']
for p in products:
    order[p['name']] = (p['price'],p['quantity'])

y = json.dumps(order)








cleaned_y = json.loads(y)


for x in cleaned_y:
    if x == "The Crown tote bag [King Collection V1]":
        print("price: ",cleaned_y['The Crown tote bag [King Collection V1]'][0])
    elif x == "Anno Domini tote bag [King Collection V1]":
        print(decimal.Decimal(cleaned_y['Anno Domini tote bag [King Collection V1]'][0]))
    elif x == "INRI tote bag":
        print(cleaned_y['INRI tote bag'][1])