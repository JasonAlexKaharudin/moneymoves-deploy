from merchants.models import webhookOrders
from api.models import orderRef

class controller:
    def __init__(self, orderID, webhookObj, orderRefObj):
        self.orderid = orderID
        self.webhook_obj = webhookObj
        self.orderRef_obj = orderRefObj