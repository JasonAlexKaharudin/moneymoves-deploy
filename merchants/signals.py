from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import webhookOrders
import api.models
import referrals.models

@receiver(post_save, sender = webhookOrders)
def post_save_webhook(sender, instance, created, *args, **kwargs):
    if created:
        #match this object with an orderRef object
        orderRef_obj = api.models.orderRef.objects.filter(merchant_name = instance.merchant)
        orderRef_obj = orderRef_obj.filter(orderID = instance.order_id)[0]
        orderRef_obj.webhook_obj = instance
        orderRef_obj.save()

        #create a new referral object
        ref_obj = referrals.models.Referral.objects.create(
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
