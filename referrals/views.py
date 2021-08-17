from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Referral
from merchants.models import Merchant
from django.contrib.auth.decorators import login_required

class ReferralListView(LoginRequiredMixin, ListView):
    model = Referral
    template_name = 'referrals/my_referrals.html'
    context_object_name = 'Referrals'
    ordering = ['-date_published']

    def get_queryset(self):
        queryset = super(ReferralListView, self).get_queryset()
        return queryset.filter(referer=self.request.user.id)

class ReferralDetailView(LoginRequiredMixin, DetailView):
    model = Referral


#this is currently not used
class CreateReferral(LoginRequiredMixin, CreateView):
    model = Referral
    fields = ['merchant', 'referee_Phone_Number', 'receipt']

    def form_valid(self, form):
        form.instance.referer = self.request.user
        form.fields['referee_Phone_Number'].required = True
        return super().form_valid(form)

@login_required
def UploadReceipt(request):
    user = User.objects.get(pk=request.user.pk)
    user_phone_num = user.profile.Phone_Number

    if request.method == "POST":
        #get the inputted phone number
        phone_input = request.POST['referee_Phone_Number']
        #handles the case when a user has not updated their phone number to their profile
        if user.profile.Phone_Number == '':
            messages.info(request, "Before you upload a receipt, please update your phone number")
            return redirect('/profile')

        #handles the case when a user enters their own phone number to the referee's phone number
        elif user_phone_num == phone_input:
            messages.info(request, "The phone number you entered is registered under your account. Please fill up a friend's phone number")
            return redirect('/referral/upload')
        
        #handles a successful case - 1. phone number filled and 2. a valid referee's phone number
        else:
            referer = user
            merchant_name = request.POST['merchant']
            friend_phone = request.POST['referee_Phone_Number']
            img = request.FILES['receipt']
            
            
            merchant = Merchant.objects.filter(name=merchant_name)[0]

            new_referral_obj = Referral.objects.create(referer = referer, referee_Phone_Number = friend_phone ,merchant = merchant, receipt = img)
            new_referral_obj.save()
            messages.success(request, "Referral created. Once we verify the transaction, you will be able to see your cashback")
            return redirect('/referral')

    context = {
        'user': user,
    }
    return render(request, 'referrals/referral_form.html', context)

