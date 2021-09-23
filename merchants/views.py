from .models import Partner_Merchant
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from webapp import settings
from .models import webhookOrders

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
def webhook_sunday_valley(request):
    shopify_hmac = request.headers.get('X-Shopify-Hmac-Sha256')  
    if verify_hmac(settings.SHOPIFY_WEBHOOK_SIGNED_KEY_SV, request.body, shopify_hmac): 
        print('Keys have been verified as valid.')  

        #get necessary data from the webhook order    
        order = request.data
        email = order['contact_email']
        location = order['billing_address']['country']    
        total_price = order['total_price']
        order_id = order['order_number']

        merchant = Partner_Merchant.objects.get(pk=1)

        obj = webhookOrders.objects.create(
            merchant=merchant,
            customer_email = email, 
            location =  location,
            order_id=order_id, 
            total_price=total_price
        )
        obj.save()

        return Response(status=status.HTTP_200_OK) 
    else:
        print('invalid')  
        return Response(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])  
def webhook_dnc(request):
    shopify_hmac = request.headers.get('X-Shopify-Hmac-Sha256')  
    if verify_hmac(settings.SHOPIFY_WEBHOOK_SIGNED_KEY_DNC, request.body, shopify_hmac): 
        print('Keys have been verified as valid.')  

        #get necessary data from the webhook order    
        order = request.data
        email = order['contact_email']
        location = order['billing_address']['country']
        total_price = order['total_price']
        order_id = order['order_number']

        merchant = Partner_Merchant.objects.get(pk=3)

        obj = webhookOrders.objects.create(
            merchant=merchant,
            customer_email = email, 
            location = location,
            order_id=order_id, 
            total_price=total_price
        )
        obj.save()

        return Response(status=status.HTTP_200_OK) 
    else:
        print('invalid')  
        return Response(status=status.HTTP_400_BAD_REQUEST)