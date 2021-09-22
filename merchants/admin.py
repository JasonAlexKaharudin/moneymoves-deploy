from django.contrib import admin
from .models import Partner_Merchant, Zalora_Brand, webhookOrders
# Register your models here.
admin.site.register(webhookOrders)
admin.site.register(Partner_Merchant)
admin.site.register(Zalora_Brand)
