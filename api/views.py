from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from webapp import settings
from .models import WebhookOrder, orderRefs

import hmac
import hashlib
import base64

def computed_hmac(secret, body):
    hash_code = hmac.new(secret.encode('utf-8'), body, hashlib.sha256)
    return base64.b64encode(hash_code.digest()).decode()

def verify_hmac(secret, body, shopify_hmac):
    return computed_hmac(secret, body) == shopify_hmac

@csrf_exempt
@api_view(['POST']) 
def ref_api(request):
    print(request.data)
    return Response(status=status.HTTP_200_OK) 


@csrf_exempt
@api_view(['POST'])  
def api_view_webhook(request):
    shopify_hmac = request.headers.get('X-Shopify-Hmac-Sha256')  
    if verify_hmac(settings.SHOPIFY_WEBHOOK_SIGNED_KEY, request.body, shopify_hmac): 
        print('Keys have been verified as valid.')  

        #get necessary data from the webhook order    
        order = request.data
        
        merchant = order['fulfillments'][0]['line_items'][0]['vendor']
        total_price = order['total_price']
        order_id = order['order_number']

        if len(order['discount_codes'][0]['code']) == 0:
            print("Order not using moneymoves discount code")
            pass 
        elif order['discount_codes'][0]['code'] == "MoneyMoves" or order['discount_codes'][0]['code'] == "MONEYMOVES" or order['discount_codes'][0]['code'] == "moneymoves":
            obj = WebhookOrder.objects.create(merchant_name=merchant, discount_code=order['discount_codes'][0]['code'], order_id=order_id, total_price=total_price)
            obj.save()
        else:
            pass

        return Response(status=status.HTTP_200_OK) 
    else:
        print('invalid')  
        return Response(status=status.HTTP_400_BAD_REQUEST)

