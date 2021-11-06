from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import Order_Controller, orderRef
from referrals.models import Referral

@receiver(post_save, sender=orderRef)
def post_save_orderRef(sender, instance, created,*args ,**kwargs):
    if created:
        if Order_Controller.objects.filter(order_id = int(instance.orderID)).exists():
            controllerObj = Order_Controller.objects.get(order_id = int(instance.orderid))
            controllerObj.orderRef_obj = instance
            controllerObj.matched = True
            controllerObj.save()
        

@receiver(post_save, sender = Order_Controller)
def post_save_webhook(sender, instance, created, *args, **kwargs):
    if instance.orderRef_obj is not None and instance.webhook is not None:
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