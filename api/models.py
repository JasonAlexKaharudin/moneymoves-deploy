from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from merchants.models import Partner_Merchant, webhookOrders
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import CASCADE
import referrals.models

class orderRef(models.Model):
    referrer = models.ForeignKey(User, on_delete=CASCADE,null=True, default=None)
    sessionID = models.IntegerField()
    orderID = models.CharField(max_length=20)
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    refereeEmail = models.EmailField(max_length=40, default = "None")
    merchant_name = models.ForeignKey(Partner_Merchant, on_delete=CASCADE, null=True, default=None)
    date_published = models.DateTimeField(default=datetime.now, blank=True)
    webhook_obj = models.ForeignKey(webhookOrders, on_delete=CASCADE, null=True, default=None)

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

class trackWidget(models.Model):
    merchant = models.ForeignKey(Partner_Merchant, on_delete=CASCADE, null = True, default = None)
    numClicks = models.IntegerField()
    date_recorded = models.DateTimeField(default = datetime.now, blank=True)

    def __str__(self):
        return f"{self.merchant}. clicks: {self.numClicks}"

@receiver(post_save, sender=orderRef)
def post_save_orderRef(sender, instance, created, *args, **kwargs):
    if created:
        #match this obj with the webhook object
        webhook_obj = webhookOrders.objects.filter(merchant = instance.merchant_name)
        webhook_obj = webhook_obj.filter(order_id = instance.orderID)[0]
        instance.webhook_obj = webhook_obj
        instance.save()

        #create a new ref object
        ref_obj = referrals.models.Referral.objects.create(
            referer_username = instance.referrer,
            merchant = instance.merchant_name,
            sessionID = instance.sessionID,
            orderID = instance.orderID,
            totalAmt = instance.totalAmt,
            products = webhook_obj.products,
            referee_email = webhook_obj.customer_email,
            orderRef_obj = instance
        )
        ref_obj.save()
        