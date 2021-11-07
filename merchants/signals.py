from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import webhookOrders
from referrals.models import Referral

@receiver(post_save, sender=webhookOrders)
def post_save_webhookOrders(sender, instance, created, *args, **kwargs):
    if created:
        if Referral.objects.filter(order_id = str(instance.order_id), merchant = instance.merchant).exists():
            controllerObj = Referral.objects.get(order_id = instance.order_id, merchant = instance.merchant)
            if controllerObj.webhook == None and controllerObj.orderRef_obj != None:
                controllerObj.webhook = instance
                controllerObj.save()
        else:
            obj = Referral.objects.create(
                referee_email = instance.customer_email,
                merchant = instance.merchant,
                orderID = str(instance.order_id),
                totalAmt = instance.total_price,
                products = instance.products,
                orderRef_obj = instance.orderRef_obj,
                webhook = instance
            )
            obj.save()