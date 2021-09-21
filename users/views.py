from django.shortcuts import render, redirect
from django.contrib import messages
from merchants.models import Partner_Merchant, Zalora_Brand
from .forms import UserUpdateForm, UserRegisterForm, PhoneForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    return render(request, 'users/home.html', {})


def brands(request):
    context = {
        'zalora': Zalora_Brand.objects.all(),
    }
    return render(request, 'users/brands.html', context)

@login_required
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method=="POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/profile')
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

            return redirect('login')
    else:
        form = UserRegisterForm()
        p_reg_form = PhoneForm()
    context = {
        'form': form,
        'p_reg_form': p_reg_form
    }
    return render(request, 'users/register.html', context)