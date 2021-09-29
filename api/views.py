from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import orderRef, invalidOrder
from referrals.models import Referral
from merchants.models import Partner_Merchant

import decimal

@api_view(['POST']) 
def ref_api(request):
    data = request.data
    
    referrer = data['username']
    referrer = User.objects.get(username = referrer)
    sessionID = data['sesh']
    orderID = data['orderID']
    totalAmt = data['amount']
    totalAmt = decimal.Decimal(totalAmt[1:])
    refereeEmail = data['email']
    merchant_name = data['merchant']

    if merchant_name == "sv":
        merchant_name = Partner_Merchant.objects.filter(pk=1)[0]
    elif merchant_name == "sp":
        merchant_name = Partner_Merchant.objects.filter(pk=2)[0]
    elif merchant_name == "dnc":
        merchant_name = Partner_Merchant.objects.filter(pk=3)[0]
    elif merchant_name == "jmc":
        merchant_name = Partner_Merchant.objects.filter(pk=4)[0]

    print("Referreal received by ",referrer)
    
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