from django.db import models
from datetime import datetime
from merchants.models import webhookOrders
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class orderRef(models.Model):
    referrer = models.ForeignKey(User, on_delete=CASCADE,null=True, default=None)
    sessionID = models.IntegerField()
    orderID = models.CharField(max_length=20)
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    refereeEmail = models.EmailField(max_length=40, default = "None")
    merchant_name = models.ForeignKey("merchants.Partner_Merchant", on_delete=CASCADE, null=True, default=None)
    date_published = models.DateTimeField(default=datetime.now, blank=True)
    webhook_obj = models.ForeignKey("merchants.webhookOrders", on_delete=CASCADE, null=True, default=None)

    class Meta:
        verbose_name_plural = "Referral Orders"

    def __str__(self):
        return f"{self.merchant_name.name} {self.orderID}. Referred by: {self.referrer.username}"

class invalidOrder(models.Model):
    referrer = models.ForeignKey(User, on_delete=CASCADE,null=True, default=None)
    sessionID = models.IntegerField()
    orderID = models.CharField(max_length=20)
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    refereeEmail = models.EmailField(max_length=40, default = "None")
    merchant_name = models.ForeignKey("merchants.Partner_Merchant", on_delete=CASCADE, null=True, default=None)
    date_published = models.DateTimeField(default=datetime.now, blank=True)
    class Meta:
        verbose_name_plural = "Invalid Referrals"
    
    def __str__(self):
        return f"Referrer: {self.referrer.email}, Referee email: {self.refereeEmail}"

class trackWidget(models.Model):
    merchant = models.ForeignKey("merchants.Partner_Merchant", on_delete=CASCADE, null = True, default = None)
    numClicks = models.IntegerField()
    date_recorded = models.DateTimeField(default = datetime.now, blank=True)

    def __str__(self):
        return f"{self.merchant}. clicks: {self.numClicks}"

class involveAsia_PostbackURL(models.Model):
    merchant = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    order_id = models.IntegerField()
    conversion_id = models.IntegerField()
    date = models.DateTimeField(default = datetime.now, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = "Involve Postback URLs"
    
    def __str__(self):
        return f"{self.merchant} #{self.order_id}"