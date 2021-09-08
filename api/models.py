from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE
from referrals.models import Referral
from django.contrib.auth.models import User

# Create your models here.
class WebhookOrder(models.Model):
    merchant_name = models.CharField(max_length=20)
    discount_code = models.CharField(max_length=12)
    order_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_published = models.DateTimeField(default=datetime.now, blank=True)
    ref_obj = models.OneToOneField(Referral, on_delete=CASCADE, null= True)

    def __str__(self):
        return f"#{self.order_id}"

class orderRefs(models.Model):
    referrer = models.CharField(max_length=20)
    sessionID = models.IntegerField()
    orderID = models.CharField(max_length=20)
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    refereeEmail = models.EmailField(max_length=40)
    merchant_name = models.CharField(max_length=20)
    
