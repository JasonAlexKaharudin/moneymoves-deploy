from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import webhookOrders
from api.models import Order_Controller

@receiver(post_save, sender=webhookOrders)
def post_save_webhookOrders(sender, instance, created, *args, **kwargs):
    if created:
        obj = Order_Controller(webhook = instance, orderRef_obj = None, order_id=instance.order_id ,matched=False)
        obj.save()