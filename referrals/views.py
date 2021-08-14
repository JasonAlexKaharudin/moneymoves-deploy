from django.db.models.expressions import F, Ref
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Referral
from django.contrib.auth.decorators import login_required
from .forms import ReferralForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Profile
from .models import Referral
from merchants.models import Merchant

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

class CreateReferral(LoginRequiredMixin, CreateView):
    model = Referral
    fields = ['merchant', 'referee_Phone_Number', 'receipt']

    def form_valid(self, form):
        form.instance.referer = self.request.user
        form.fields['referee_Phone_Number'].required = True
        return super().form_valid(form)

def UploadReceipt(request):
    user = User.objects.get(pk=request.user.pk)
  
    if request.method == "POST":
        if user.profile.Phone_Number == '':
            messages.info(request, "Please fill up your phone number in the profile page")
            return redirect('/profile')
        else:
            referer = user
            merchant = request.POST['merchant']
            img = request.POST['receipt']
            new_referral_obj = Referral.create(referer = referer, merchant = merchant, receipt = img)
            new_referral_obj.save()
            messages.success(request, "Referral created. Once we verify the transaction, you will be able to see your cashback")
            return redirect('/referral')

    context = {
        'user': user,
    }
    return render(request, 'users/referral_form.html', context)