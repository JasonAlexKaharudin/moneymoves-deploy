from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import webhookOrders
from api.models import Order_Controller

@receiver(post_save, sender=webhookOrders)
def post_save_webhookOrders(sender, instance, created, *args, **kwargs):
    if created:
        if Order_Controller.objects.filter(order_id = instance.order_id).exists():
            print("found a matching order_controller obj")
            controllerObj = Order_Controller.objects.get(order_id = instance.order_id)
            if controllerObj.webhook == None:
                controllerObj.webhook = instance
                controllerObj.matched = True
            controllerObj.save()