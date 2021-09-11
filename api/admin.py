from django.contrib import admin
from .models import WebhookOrder, orderRef

# Register your models here.
admin.site.register(WebhookOrder)
admin.site.register(orderRef)