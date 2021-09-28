from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login
from django.utils import html
from merchants.models import Zalora_Brand, Partner_Merchant
from .forms import UserUpdateForm, UserRegisterForm, PhoneForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from webapp import settings

def home(request):
    context = {
        'zalora': Zalora_Brand.objects.all(),
        'partner': Partner_Merchant.objects.all()
    }
    return render(request, 'users/home.html', context)

def brands(request):
    context = {
        'zalora': Zalora_Brand.objects.all(),
        'partner': Partner_Merchant.objects.all()
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
            messages.add_message(request, constants.SUCCESS, f"Account created for '{username}'.")
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )

            subject = 'Thank you for signing up!'
            html_message = render_to_string('users/register_email.html', {'username': username})
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = user.email
            mail.send_mail(subject, plain_message, from_email,[to], html_message = html_message)

            login(request, new_user)
            return redirect('brands page')
    else:
        form = UserRegisterForm()
        p_reg_form = PhoneForm()
    context = {
        'form': form,
        'p_reg_form': p_reg_form
    }
    return render(request, 'users/register.html', context)