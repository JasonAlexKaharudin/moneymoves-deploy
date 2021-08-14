from django import forms
from .models import Referral

class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['merchant', 'referee_Phone_Number', 'receipt']