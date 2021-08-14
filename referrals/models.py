from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from merchants.models import Merchant
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from users.models import Profile

# Create your models here.
class Referral(models.Model):
    referer = models.ForeignKey(User, on_delete=CASCADE, related_name="referer")
    referee_Phone_Number = PhoneNumberField(blank=True)
    merchant = models.ForeignKey(Merchant ,on_delete=CASCADE)
    referer_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referee_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    receipt = models.ImageField(default = 'default.jpg', upload_to='receipts')
    is_Verified = models.BooleanField(default=False) #if verified is true then show cashback earned on profile
    is_Published = models.BooleanField(default=False) # for admins to check which has been paylah-ed
    date_published = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):
        return reverse('referrals:referral-list')