from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Referral
from users.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def wallet_referrals(request):
    refers = Referral.objects.filter(referer_username = request.user.pk)
    referred = Referral.objects.filter(referee_email = request.user.email)
    context = {
        'refers': refers,
        'referred': referred
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

        #handles a successful case: 1. phone number filled and 2. a valid referee's phone number
        elif len(phone_input) != 11:
            messages.info(request, "Please enter a Singapore number (8 digits) without the country code")
            return redirect('/referral/upload')
        else:
            referer = user
            friend_phone = request.POST['referee_Phone_Number']
            
            img = request.FILES['receipt']

            #check if the referee phone number has an account with us
            #if the referee has an account, create a new referral obj with referee_username as friend phone
            if Profile.objects.filter(Phone_Number=friend_phone).exists():
                for user in list(User.objects.all()):
                    if user.profile.Phone_Number == friend_phone:
                        friend_username = user.username
                        new_ref_obj = Referral.objects.create(referer = referer, referee_Phone_Number = friend_phone ,  referee_username = friend_username ,receipt = img)
                        new_ref_obj.save()
                        break
            else:
                new_referral_obj = Referral.objects.create(referer = referer, referee_Phone_Number = friend_phone , receipt = img)
                new_referral_obj.save()
                new_orphan = OrphanList.objects.create(Phone_Number=friend_phone, referral_obj=new_referral_obj)
                new_orphan.save()


            messages.success(request, "Referral created. Once we verify the transaction, you will be able to see your cashback")
            return redirect('/referral')

    context = {
        'user': user,
    }
    return render(request, 'referrals/referral_form.html', context)

