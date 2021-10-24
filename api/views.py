from django.db import connections
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import orderRef, invalidOrder, trackWidget
from merchants.models import Partner_Merchant
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
def links_generated(request):
    data = request.data
    username = data['username'];
    clicks = data['clicks'];
    print(clicks)
    
    if User.objects.filter(username = username).exists():
        curr_user = User.objects.get(username = username)
        curr_user.profile.links_created = curr_user.profile.links_created + 1;
        curr_user.profile.save()
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

#post back URL view
def involveAsia(request):
    user_id = request.GET['uid']
    order_id = int(request.GET['order_id']) 
    amount = int(request.GET['amt'])
    
    date = request.GET['date']
    merchant = request.GET['merchant']
    conversion_id = request.GET['cid']

    # obj = involveAsia_PostbackURL.objects.create(
    #     merchant = merchant,
    #     user_id = user_id,
    #     order_id = order_id,
    #     conversion_id = conversion_id,
    #     date = date,
    #     amt = amount
    # )
    # obj.save()

    return render(request, 'users/home.html', {})