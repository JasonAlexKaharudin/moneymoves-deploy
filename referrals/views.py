from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Referral, orphanReceipt, receipts
from users.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def wallet_referrals(request):
    refers = Referral.objects.filter(referer_username = request.user.pk)
    referred = Referral.objects.filter(referee_email = request.user.email)
    receipt = receipts.objects.filter(referer = request.user.pk)
    referred_receipt = receipts.objects.filter(referee_phone = request.user.profile.Phone_Number)
    context = {
        'refers': refers,
        'referred': referred,
        'receipt': receipt,
        'ref_receipt': referred_receipt
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
        
        if user_phone_num == phone_input:
            messages.info(request, "The phone number you entered is registered under your account. Please fill up a friend's phone number")
            return redirect('/referral/upload')
        else:
            referer = user
            friend_phone = request.POST['referee_Phone_Number']
            img = request.FILES['receipt']

            #check if the referee phone number has an account with us
            #if the referee has an account, create a new referral obj with referee_username as friend phone
            if Profile.objects.filter(Phone_Number=friend_phone).exists():
                referee_profile = Profile.objects.get(Phone_Number = friend_phone)
                referee_username = referee_profile.user.username
                new_receipt_obj = receipts.objects.create(
                    referer = referer,
                    referee_phone = referee_profile.Phone_Number,
                    referee = referee_username,
                    cashback = 0,
                    receipt_img = img
                )
                new_receipt_obj.save()
            else:
                new_receipt_obj = receipts.objects.create(
                    referer = referer,
                    referee_phone = phone_input,
                    referee = "No account. See Orphan List for associated order",
                    cashback = 0,
                    receipt_img = img
                )
                new_receipt_obj.save()

                new_orphanReceipt = orphanReceipt.objects.create(
                    referer = referer,
                    referee = phone_input,
                    referral_obj = new_receipt_obj
                )
                new_orphanReceipt.save()

            messages.success(request, "Referral created. Once we verify the transaction, you will be able to see your cashback")
            return redirect('/referral')

    context = {
        'user': user,
    }
    return render(request, 'referrals/referral_form.html', context)

