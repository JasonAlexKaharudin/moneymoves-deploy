from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import Profile
from phonenumber_field.modelfields import PhoneNumberField

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email' , 'class': 'inputs'}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'inputs'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'inputs'}))
    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'inputs'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Phone_Number']
        widgets = {
            'Phone_Number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'inputs'})
        }