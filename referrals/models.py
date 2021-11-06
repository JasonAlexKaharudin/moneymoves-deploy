from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from phonenumber_field.modelfields import PhoneNumberField
import merchants.models
import api.models
from datetime import datetime

def jsonfield_default_value(): 
    productList = {
        "product": 0
    }
    return productList

class receipts(models.Model):
    referer = models.ForeignKey(User, on_delete=CASCADE, related_name="RefererReceipts", null=True)
    referee_phone = PhoneNumberField(null=True, blank=True)
    referee = models.CharField(max_length=150, default="None", null=True)
    cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    receipt_img = models.ImageField()
    date_published = models.DateTimeField(default=datetime.now, blank=True)
    
    class Meta:
        verbose_name_plural = "Uploaded Receipts"

    def __str__(self):
        return f"Receipt by {self.referer} at {self.date_published}"

class orphanReceipt(models.Model):
    referer = models.ForeignKey(User, on_delete=CASCADE, null=True)
    referee = models.CharField(max_length=50, default=0)
    referral_obj = models.OneToOneField(receipts, on_delete=CASCADE, default=None, null=True)

    def __str__(self):
        return f"Referral by {self.referer}"

# Create your models here.
class Referral(models.Model):
    referer_username = models.ForeignKey(User, on_delete=CASCADE, related_name="referer", null=True)
    merchant = models.ForeignKey(merchants.models.Partner_Merchant ,on_delete=CASCADE, null=True)
    sessionID = models.IntegerField(default=0)
    orderID = models.CharField(max_length=20, default=0)  
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    products = models.JSONField(default = jsonfield_default_value, null=True)
    referer_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referee_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referee_email = models.EmailField(max_length=50, default="None")
    referee_username = models.CharField(max_length=40, default="Not Signed Up")
    is_Verified = models.BooleanField(default=False)
    stored_in_wallet = models.BooleanField(default=False)
    referee_has_account = models.BooleanField(default=False)
    orderRef_obj = models.OneToOneField(api.models.orderRef, on_delete=CASCADE, null=True, default=None)
    date_published = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):
        return reverse('referrals:referral-list')

    def __str__(self):
        return f"{self.merchant.name} {self.orderID}. Referred by: {self.referer_username.username}"

class OrphanList(models.Model):
    refereeEmail = models.EmailField(max_length=40, default=0)
    referee_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referral_obj = models.OneToOneField(Referral, on_delete=CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.merchant.name} {self.orderID}. Referred by: {self.referer_username.username}"   