import json

file = open('webhookOrder.json',)
data = json.load(file)

# print(data['line_items'][0]['name'])
# print(data['line_items'][0]['price'])


products = data['line_items']

order = {
    "INRI tote bag": "50.00", 
    "The Crown tote bag [King Collection V1]": "50.00"
}

for p in order:
    
    if p == "The Crown tote bag [King Collection V1]":
        print(order['The Crown tote bag [King Collection V1]'])
    elif p == "Anno Domini tote bag [King Collection V1]":
        print("price of Domini:", order['Anno Domini tote bag [King Collection V1]'])
    elif p == "INRI tote bag":
        print(order['INRI tote bag'])