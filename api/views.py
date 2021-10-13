from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import orderRef, invalidOrder, trackWidget
from merchants.models import Partner_Merchant, webhookOrders
import time
import decimal

@api_view(['POST']) 
def widget(request):
    data = request.data

    numofclicks = data['clicks']
    merchant = Partner_Merchant.objects.get(name = data['merchant'])
    tracking = trackWidget.objects.create(
        merchant = merchant,
        numClicks = numofclicks
    )
    tracking.save()
    return Response(status=status.HTTP_200_OK) 

@api_view(['POST']) 
def ref_api(request):
    data = request.data
    
    referrer = data['username']
    referrer = User.objects.get(username = referrer)
    sessionID = data['sesh']

    orderID = data['orderID']
    orderID = orderID.split(" ")
    orderID = orderID[1]
    orderID = orderID.replace("#", "")
    
    refereeEmail = data['email']
    merchant_name = data['merchant']
    merchant_name = Partner_Merchant.objects.get(name = merchant_name)

    if referrer.email == refereeEmail:
        #invalid referral. Referee email must be different from your account.
        invalidOrder_obj = invalidOrder.objects.create(
            referrer = referrer,
            sessionID = sessionID, 
            orderID = orderID, 
            totalAmt = 0, 
            refereeEmail = refereeEmail, 
            merchant_name = merchant_name 
        )
        invalidOrder_obj.save()
    else:
        time.sleep(3)
        # create new orderRef object, create new ReferralObj
        orderRef_obj = orderRef.objects.create(
            referrer = referrer,
            sessionID = sessionID, 
            orderID = orderID, 
            totalAmt = decimal.Decimal(0), 
            refereeEmail = refereeEmail, 
            merchant_name = merchant_name,
            webhook_obj = None
        )
        orderRef_obj.save()

    return Response(status=status.HTTP_200_OK) 