from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import webhookOrders
from api.models import Order_Controller

@receiver(post_save, sender=webhookOrders)
def post_save_webhookOrders(sender, instance, created, *args, **kwargs):
    if created:
        if Order_Controller.objects.filter(order_id = instance.order_id).exists():
            controllerObj = Order_Controller.objects.get(order_id = instance.order_id)
            if controllerObj.webhook == None and controllerObj.orderRef_obj != None:
                controllerObj.webhook = instance
                controllerObj.matched = True
                controllerObj.save()
        else:
            # create a new order_controller object named obj
            obj = Order_Controller(
                    webhook = instance,
                    orderRef_obj = None, 
                    order_id = instance.order_id,
                    matched = False
                )
            obj.save()