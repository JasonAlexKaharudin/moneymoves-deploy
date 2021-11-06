from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order_Controller, orderRef
from referrals.models import Referral

@receiver(post_save, sender=orderRef)
def post_save_orderRef(sender, instance, created,*args ,**kwargs):
    if created:
        obj = Order_Controller.objects.create(
            webhook = None,
            orderRef_obj = instance,
            order_id = int(instance.orderID),
            matched = False
        )
        obj.save()
        

@receiver(post_save, sender = Order_Controller)
def post_save_order_controller(sender, instance, created, *args, **kwargs):
    if instance.orderRef_obj != None and instance.webhook != None:
        print("orderRef and webhook match, now creating referral obj")
        ref_obj = Referral.objects.create(
            referer_username = instance.orderRef_obj.referrer,
            merchant = instance.webhook.merchant,
            sessionID = instance.orderRef_obj.sessionID,
            orderID = instance.webhook.order_id,
            totalAmt = instance.webhook.total_price,
            products = instance.webhook.products,
            referee_email = instance.webhook.customer_email,
            orderRef_obj = instance.orderRef_obj
        )
        ref_obj.save()