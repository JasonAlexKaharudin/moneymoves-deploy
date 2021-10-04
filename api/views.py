from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import orderRef, invalidOrder, trackWidget
from referrals.models import Referral
from merchants.models import Partner_Merchant
from merchants.models import webhookOrders

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
    refereeEmail = data['email']
    merchant_name = data['merchant']
    merchant_name = Partner_Merchant.objects.get(name = merchant_name)

    # match the webhook object with merchant name first then filter the referee email with the latest webhook obj
    webhooks = webhookOrders.objects.filter(merchant = merchant_name)
    obj = webhooks.filter(customer_email = refereeEmail).latest('date_published')
    orderID = obj.order_id
    products = obj.products
    totalAmt = decimal.Decimal(obj.total_price)

    print("Referreal received by",referrer)

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
            merchant_name = merchant_name,
            webhook_obj = obj
        )
        orderRef_obj.save()

        referral_obj = Referral.objects.create(
            referer_username = referrer,
            merchant = merchant_name,
            sessionID = sessionID,
            orderID = orderID,
            totalAmt = totalAmt,
            referee_email = refereeEmail,
            products = products,
            orderRef_obj = orderRef_obj
        )
        referral_obj.save()

    return Response(status=status.HTTP_200_OK) 