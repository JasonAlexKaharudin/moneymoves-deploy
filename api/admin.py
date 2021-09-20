from django.contrib import admin
from .models import WebhookOrder, orderRef, invalidOrder

# Register your models here.
admin.site.register(WebhookOrder)
admin.site.register(orderRef)
admin.site.register(invalidOrder)