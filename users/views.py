from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from merchants.models import Merchant
from django.contrib.auth.models import User
from .models import Profile

def home(request):
    return render(request, 'users/home.html', {})

class BrandListView(ListView):
    model = Merchant
    template_name = 'users/brands.html'
    context_object_name = 'Brands'

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

@login_required
def phone(request):
    user = User.objects.get(pk=request.user.pk).profile
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        if Profile.objects.filter(Phone_Number=phone_number).exists():
            messages.info(request, f"The phone number '{phone_number}' has been taken")
            return redirect('phone')
        else:
            user.Phone_Number = phone_number
            user.save()
            messages.success(request, f"Updated phone number successfully!")
            return redirect('/phone')
    return render(request, 'users/phone.html', {})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']
        form = UserRegisterForm(request.POST)
    
        # check if the two passwords are the same
        if pw1 != pw2:
            messages.info(request, "Passwords do not match. Please make sure that your password is not similar to your username or email. Passwords must be minimum 8 characters long")
            return redirect('register')

        # check if username exists
        elif User.objects.filter(username= username).exists():
            messages.info(request, f"The Username '{username}' has been taken")
            return redirect('register')

        # check if email already exists
        elif User.objects.filter(email=email).exists():
            messages.info(request, f"The email '{email}' already has an account")
            return redirect('register')
        
        # check if
        elif form.is_valid():
            form.save()    
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for '{username}'. Please enter your phone number to get your cashback!")       
            return redirect('/login')
        
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})