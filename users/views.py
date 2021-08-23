from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from .forms import UserRegisterForm, UserUpdateForm, PhoneForm
from django.contrib.auth.decorators import login_required
from merchants.models import Merchant
from django.contrib.auth.models import User
from .models import OrphanList
from referrals.models import Referral

def home(request):
    return render(request, 'users/home.html', {})

class BrandListView(ListView):
    model = Merchant
    template_name = 'users/brands.html'
    context_object_name = 'Brands'

def brands(request):
    return render(request, 'users/brands.html', {})

@login_required
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method=="POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/referral/upload')
    else:
        u_form = UserUpdateForm(instance=request.user)


    context = {
        'user': user,
        'u_form': u_form,
    }

    return render(request, 'users/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_reg_form = PhoneForm(request.POST)
        if form.is_valid() and p_reg_form.is_valid():
            user = form.save()
            #user.refresh_from_db()  # load the profile instance created by the signal
            p_reg_form = p_reg_form.save(commit=False)
            p_reg_form.user = user
            p_reg_form.save()

            username = user.username
            messages.success(request, f"Account created for '{username}', login to start Earning!")       

            phone_num = request.POST['Phone_Number']
            #check orphan list and populate if there is any matching phone number
            if OrphanList.objects.filter(Phone_Number=phone_num).exists():
                for orphan in OrphanList.objects.filter(Phone_Number=phone_num):
                    if orphan.Phone_Number == phone_num:
                        ref_obj = orphan.referral_obj
                        ref_obj.referee_username = username
                        ref_obj.save()
                        orphan.delete()

            return redirect('login')
    else:
        form = UserRegisterForm()
        p_reg_form = PhoneForm()
    context = {
        'form': form,
        'p_reg_form': p_reg_form
    }
    return render(request, 'users/register.html', context)