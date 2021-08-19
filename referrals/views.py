from users.views import phone
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Referral
from users.models import OrphanList
from merchants.models import Merchant
from django.contrib.auth.decorators import login_required

@login_required
def wallet_referrals(request):
    curr_user = User.objects.get(pk=request.user.pk)
    curr_user_profile = curr_user.profile

    # get the referral list for this user
    user_referrals = list(Referral.objects.filter(referer = curr_user))

    # get the verified referral list for this user
    user_verified_referrals = list(Referral.objects.filter(referer = curr_user, is_Verified = True))

    #update the amount of referrals this user has and save the object
    curr_user_profile.num_of_refers = len(user_verified_referrals)
    curr_user_profile.save()

    # get the amount referred for this user
    user_referred = list(Referral.objects.filter(referee_username=curr_user.username))

    context = {
        'profile': curr_user_profile,
        'referrals': user_referrals, 
        'user_referred': user_referred,
    }
    return render(request, 'referrals/my_referrals.html', context)


class ReferralDetailView(LoginRequiredMixin, DetailView):
    model = Referral


@login_required
def UploadReceipt(request):
    user = User.objects.get(pk=request.user.pk)
    user_phone_num = user.profile.Phone_Number

    if request.method == "POST":
        #get the inputted phone number
        phone_input = request.POST['referee_Phone_Number']
        phone_input = "+65" + phone_input
        
        #handles the case when a user has not updated their phone number to their profile
        if user.profile.Phone_Number == '':
            messages.info(request, "Before you upload a receipt, please update your phone number")
            return redirect('/profile')

        #handles the case when a user enters their own phone number to the referee's phone number
        elif user_phone_num == phone_input:
            messages.info(request, "The phone number you entered is registered under your account. Please fill up a friend's phone number")
            return redirect('/referral/upload')
        #handles a successful case - 1. phone number filled and 2. a valid referee's phone number
        elif len(phone_input) != 11:
            messages.info(request, "Please enter a Singapore number without the country code")
            return redirect('/referral/upload')
        else:
            referer = user
            merchant_name = request.POST['merchant']
            friend_phone = request.POST['referee_Phone_Number']
            img = request.FILES['receipt']

            #gets the merchant name 
            merchant = Merchant.objects.filter(name=merchant_name)[0]

            #check if the referee phone number has an account with us
            for x in User.objects.all():
                #if the referee has an account with us
                if x.profile.Phone_Number == friend_phone:
                    friend_username = x.username
                    new_referral_obj = Referral.objects.create(referer = referer, referee_Phone_Number = friend_phone ,merchant = merchant,  referee_username = friend_username ,receipt = img)
                    new_referral_obj.save()
                    break
                #if the referee has an account but has not updated their phone
                elif x.profile.Phone_Number == '':
                    continue
                #if the referee does not have an account at all
                else:
                    new_referral_obj = Referral.objects.create(referer = referer, referee_Phone_Number = friend_phone ,merchant = merchant, receipt = img)
                    new_referral_obj.save()
                    new_orphan = OrphanList.objects.create(Phone_Number=friend_phone, referral_obj=new_referral_obj)
                    new_orphan.save()
                    break

            messages.success(request, "Referral created. Once we verify the transaction, you will be able to see your cashback")
            return redirect('/referral')

    context = {
        'user': user,
    }
    return render(request, 'referrals/referral_form.html', context)

