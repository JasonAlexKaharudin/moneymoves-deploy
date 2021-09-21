from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from merchants.models import Partner_Merchant
from django.db.models.deletion import CASCADE

# Create your models here.
class WebhookOrder(models.Model):
    merchant_name = models.CharField(max_length=40)
    discount_code = models.CharField(max_length=12)
    order_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_published = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"Order ID: #{self.order_id}"

class orderRef(models.Model):
    referrer = models.ForeignKey(User, on_delete=CASCADE,null=True, default=None)
    sessionID = models.IntegerField()
    orderID = models.CharField(max_length=20)
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    refereeEmail = models.EmailField(max_length=40, default = "None")
    merchant_name = models.ForeignKey(Partner_Merchant, on_delete=CASCADE, null=True, default=None)
    date_published = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.merchant_name.name} {self.orderID}. Referred by: {self.referrer.username}"

class invalidOrder(models.Model):
    referrer = models.ForeignKey(User, on_delete=CASCADE,null=True, default=None)
    sessionID = models.IntegerField()
    orderID = models.CharField(max_length=20)
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    refereeEmail = models.EmailField(max_length=40, default = "None")
    merchant_name = models.ForeignKey(Partner_Merchant, on_delete=CASCADE, null=True, default=None)
    date_published = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"Referrer: {self.referrer.email}, Referee email: {self.refereeEmail}"