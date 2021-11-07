from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order_Controller, orderRef
from referrals.models import Referral

@receiver(post_save, sender=orderRef)
def post_save_orderRef(sender, instance, created,*args ,**kwargs):
    if created:
        if Referral.objects.filter(orderID = instance.orderID, merchant = instance.merchant_name).exists():
            controllerObj = Referral.objects.get(orderID = instance.orderID, merchant = instance.merchant_name)
            if controllerObj.orderRef_obj == None and controllerObj.webhook != None:
                controllerObj.orderRef_obj = instance
                controllerObj.save()
        else:
            obj = Referral.objects.create(
                referer_username = instance.referrer,
                merchant = instance.merchant_name,
                sessionID = instance.sessionID,
                orderID = instance.orderID,
                totalAmt = instance.totalAmt,
                products = {"product": 0},
                referee_email = "None",
                orderRef_obj = instance.orderRef_obj,
                webhook = None
            )
            obj.save()