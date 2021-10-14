from typing import OrderedDict
from django.db import models
from datetime import datetime
import api.models
import referrals.models
from django.db.models.deletion import CASCADE
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

# Create your models here.
class Partner_Merchant(models.Model):
    name = models.CharField(max_length=200)
    date_joined = models.DateTimeField("Date Joined")
    store_link = models.URLField(max_length=200, null = True)
    img_link = models.URLField(max_length=200, null = True)
    cashback_amt = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Partner Merchants"

    def __str__(self):
        return self.name

def jsonfield_default_value(): 
    productList = {
        "product": 0
    }
    return productList

class webhookOrders(models.Model):
    merchant = models.ForeignKey(Partner_Merchant, on_delete=CASCADE)
    order_id = models.IntegerField()
    customer_email = models.EmailField(max_length=60, default = "None")
    location = models.CharField(max_length=20, default="SG")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    products = models.JSONField(default = jsonfield_default_value, null=True)
    date_published = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.merchant.name} order ID: #{self.order_id}"

@receiver(post_save, sender = webhookOrders)
def post_save_webhook(sender, instance, created, *args, **kwargs):
    if created:
        #match this object with an orderRef object
        orderRef_obj = api.models.orderRef.objects.filter(merchant_name = instance.merchant)
        orderRef_obj = orderRef_obj.filter(orderID = instance.order_id)[0]
        orderRef_obj.webhook_obj = instance
        orderRef_obj.save()

        #create a new referral object
        ref_obj = referrals.models.Referral.create(
            referer_username = orderRef_obj.referrer,
            merchant = instance.merchant,
            sessionID = orderRef_obj.sessionID,
            orderID = instance.order_id,
            totalAmt = instance.total_price,
            products = instance.products,
            referee_email = instance.customer_email,
            orderRef_obj = orderRef_obj
        )

        ref_obj.save()
        instance.save()


class Amazon_Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_link = models.CharField(max_length=500, default="None")
    cashback_amt = models.IntegerField(default=0)
    img_link = models.URLField(max_length=300)

    class Meta:
        verbose_name_plural = "Amazon Merchants"

    def __str__(self):
        return self.brand_name