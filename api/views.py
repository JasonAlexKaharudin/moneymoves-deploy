from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from webapp import settings
from django.contrib.auth.models import User
from .models import WebhookOrder, orderRef, invalidOrder
from referrals.models import Referral
from merchants.models import Merchant

import hmac
import hashlib
import base64
import decimal

@api_view(['POST']) 
def ref_api(request):
    data = request.data
    
    referrer = data['username']
    referrer = User.objects.filter(username = referrer)[0]
    sessionID = data['sesh']
    orderID = data['orderID']
    totalAmt = data['amount']
    totalAmt = decimal.Decimal(totalAmt[1:])
    refereeEmail = data['email']
    merchant_name = data['merchant']

    if merchant_name == "sv":
        merchant_name = Merchant.objects.filter(pk=1)[0]
    elif merchant_name == "sp":
        merchant_name = Merchant.objects.filter(pk=2)[0]
    elif merchant_name == "dnc":
        merchant_name = Merchant.objects.filter(pk=3)[0]
    
    if referrer.email == refereeEmail:
        #invalid referral. Referee email must be different from your account.
        invalidOrder_obj = invalidOrder.objects.create(
            referrer = referrer,
            sessionID = sessionID, 
            orderID = orderID, 
            totalAmt = totalAmt, 
            refereeEmail = refereeEmail, 
            merchant_name = merchant_name 
        )
        invalidOrder_obj.save()
    else:
        # create new orderRef object, create new ReferralObj
        orderRef_obj = orderRef.objects.create(
            referrer = referrer,
            sessionID = sessionID, 
            orderID = orderID, 
            totalAmt = totalAmt, 
            refereeEmail = refereeEmail, 
            merchant_name = merchant_name
        )
        orderRef_obj.save()

        referral_obj = Referral.objects.create(
            referer_username = referrer,
            merchant = merchant_name,
            sessionID = sessionID,
            orderID = orderID,
            totalAmt = totalAmt,
            referee_email = refereeEmail,
            orderRef_obj = orderRef_obj
        )
        referral_obj.save()

    return Response(status=status.HTTP_200_OK) 



def computed_hmac(secret, body):
    hash_code = hmac.new(secret.encode('utf-8'), body, hashlib.sha256)
    return base64.b64encode(hash_code.digest()).decode()

def verify_hmac(secret, body, shopify_hmac):
    return computed_hmac(secret, body) == shopify_hmac

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

